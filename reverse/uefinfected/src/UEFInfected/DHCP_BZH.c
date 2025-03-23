#include "DHCP_BZH.h"



EFI_STATUS GetDhcp4Address(EFI_HANDLE ImageHandle, EFI_IPv4_ADDRESS *ClientIp) {
    EFI_STATUS Status;
    EFI_DHCP4_PROTOCOL *Dhcp4;
    EFI_SERVICE_BINDING_PROTOCOL *Dhcp4ServiceBinding;
    EFI_HANDLE Dhcp4ChildHandle = NULL;
    EFI_DHCP4_MODE_DATA Dhcp4ModeData;
    EFI_DHCP4_CONFIG_DATA CfgData;
  
    // Find DHCP4
    Status = gBS->LocateProtocol(&gEfiDhcp4ServiceBindingProtocolGuid, NULL, (VOID **)&Dhcp4ServiceBinding);
    if (EFI_ERROR(Status)) {
        Print(L"Failed to locate DHCP4 service: %r\n", Status);
        return Status;
    }
  
    // Create child DHCP4
    Status = Dhcp4ServiceBinding->CreateChild(Dhcp4ServiceBinding, &Dhcp4ChildHandle);
    if (EFI_ERROR(Status)) {
        Print(L"Failed to create DHCP4 child: %r\n", Status);
        return Status;
    }
  
    // Open DHCP4 protocol
    Status = gBS->HandleProtocol(Dhcp4ChildHandle, &gEfiDhcp4ProtocolGuid, (VOID **)&Dhcp4);
    if (EFI_ERROR(Status)) {
        Print(L"Failed to open DHCP4 protocol: %r\n", Status);
        Dhcp4ServiceBinding->DestroyChild(Dhcp4ServiceBinding, Dhcp4ChildHandle);
        return Status;
    }
  
    // DHCP edk2's stack configuration
    EFI_IPv4_ADDRESS dDiscoverIP  = { .Addr = {0, 0, 0, 0} }; // DHCP discover
    CfgData.ClientAddress =  dDiscoverIP;
    CfgData.DiscoverTryCount = 0;
    CfgData.DiscoverTimeout = NULL;
    CfgData.RequestTryCount = 0;
    CfgData.RequestTimeout = NULL;
    CfgData.Dhcp4Callback = NULL;
    CfgData.OptionCount = 0;
  
    // Configure DHCP
    Status = Dhcp4->Configure(Dhcp4, &CfgData);
    if (EFI_ERROR(Status)) {
        Print(L"Failed to configure DHCP: %r\n", Status);
        return Status;
    }
  
  
    // Start DHCP
    Status = Dhcp4->Start(Dhcp4, NULL);
    if (EFI_ERROR(Status)) {
        Print(L"Failed to start DHCP4: %r\n", Status);
        Dhcp4ServiceBinding->DestroyChild(Dhcp4ServiceBinding, Dhcp4ChildHandle);
        return Status;
    }
  
    // 10 retries to get IPv4 (polling)
    UINTN Retries = 10;
    while (Retries--) {
        Status = Dhcp4->GetModeData(Dhcp4, &Dhcp4ModeData);
        if (!EFI_ERROR(Status) && Dhcp4ModeData.State == Dhcp4Bound) {
            CopyMem(ClientIp, &Dhcp4ModeData.ClientAddress, sizeof(EFI_IPv4_ADDRESS));
            //Print(L"DHCP IP Address: %d.%d.%d.%d\n", 
            //    ClientIp->Addr[0], ClientIp->Addr[1], ClientIp->Addr[2], ClientIp->Addr[3]);
            break;
        }
        gBS->Stall(1000000); // Wait 1 second
    }

    // No DHCP server ?
    if (Retries == 0) {
        Print(L"Failed to obtain IP via DHCP\n");
        return EFI_TIMEOUT;
    }
  
    return EFI_SUCCESS;
  }