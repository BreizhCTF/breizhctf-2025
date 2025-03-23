#pragma once
#include <Uefi.h>
#include <Protocol/SimpleFileSystem.h>
#include <Protocol/BlockIo.h>
#include <Guid/FileInfo.h>
#include <Library/UefiBootServicesTableLib.h> // gBS
#include <Library/MemoryAllocationLib.h>

#include "RC4_BZH.h"


EFI_STATUS initEncryption(UINT8* Rc4Key, UINT8* Rc4KeyEncrypted);