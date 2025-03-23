#pragma once

#include <Uefi.h>
#include <Library/UefiLib.h>
#include <Protocol/Dhcp4.h>
#include <Protocol/ServiceBinding.h>
#include <Library/UefiBootServicesTableLib.h>
#include <Library/BaseMemoryLib.h>


EFI_STATUS GetDhcp4Address(EFI_HANDLE ImageHandle, EFI_IPv4_ADDRESS *ClientIp);