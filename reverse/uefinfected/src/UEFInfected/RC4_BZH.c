#include "RC4_BZH.h"


// RC4 Key Scheduling Algorithm (KSA)
VOID Rc4Init(UINT8 *S, UINT8 *Key, UINTN KeyLen) {
    UINTN i, j = 0;
    UINT8 Temp;
  
    for (i = 0; i < 256; i++) {
        S[i] = (UINT8)i;
    }
  
    for (i = 0; i < 256; i++) {
        j = (j + S[i] + Key[i % KeyLen]) % 256;
        Temp = S[i];
        S[i] = S[j];
        S[j] = Temp;
    }
  }

// RC4 Pseudo-Random Generation Algorithm (PRGA)
VOID Rc4Encrypt(UINT8 *S, UINT8 *Data, UINTN DataLen) {
  UINTN i = 0, j = 0, k;
  UINT8 Temp;

  for (k = 0; k < DataLen; k++) {
      i = (i + 1) % 256;
      j = (j + S[i]) % 256;
      
      Temp = S[i];
      S[i] = S[j];
      S[j] = Temp;

      Data[k] ^= S[(S[i] + S[j]) % 256];
  }
}

// Génère une clé RC4 aléatoire avec EFI_RNG_PROTOCOL
EFI_STATUS GenerateRc4Key(UINT8 *Key, UINTN KeySize) {
  EFI_STATUS Status;
  EFI_RNG_PROTOCOL *RngProtocol;

  Status = gBS->LocateProtocol(&gEfiRngProtocolGuid, NULL, (VOID **)&RngProtocol);
  if (EFI_ERROR(Status)) {
      Print(L"Erreur : Impossible d'obtenir EFI_RNG_PROTOCOL\n");
      return Status;
  }

  return RngProtocol->GetRNG(RngProtocol, NULL, KeySize, Key);
}