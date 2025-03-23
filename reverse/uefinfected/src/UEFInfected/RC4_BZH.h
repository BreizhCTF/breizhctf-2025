#pragma once

#include <Uefi.h>
#include <Protocol/ServiceBinding.h>
#include <Library/UefiBootServicesTableLib.h> // gBS
#include <Protocol/Rng.h>
#include <Library/UefiLib.h>

#define RC4_KEY_SIZE 16  // 128 bits

EFI_STATUS GenerateRc4Key(UINT8 *Key, UINTN KeySize);
VOID Rc4Encrypt(UINT8 *S, UINT8 *Data, UINTN DataLen);
VOID Rc4Init(UINT8 *S, UINT8 *Key, UINTN KeyLen);