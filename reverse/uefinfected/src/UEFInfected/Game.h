#pragma once


#include <Uefi.h>
#include <Library/UefiBootServicesTableLib.h>
#include <Library/UefiLib.h>
#include <Library/BaseLib.h>
#include <Library/BaseMemoryLib.h>

BOOLEAN PlayerMove(UINT8* X, UINT8* Y);
BOOLEAN HackerMove (UINT8 X, UINT8 Y);


