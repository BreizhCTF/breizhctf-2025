package com.example.finisteg;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;


public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        Button checkButton = findViewById(R.id.check_button);
        EditText flagInput = findViewById(R.id.flagInput);


        // Charger l'image depuis drawable
        BitmapFactory.Options o = new BitmapFactory.Options();
        o.inScaled = false;
        Bitmap bm = BitmapFactory.decodeResource(getResources(), R.drawable.breizhctf_logo,o);


        checkButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String userFlag = flagInput.getText().toString();
                String ex = decodeBase64(extractTextFromImage(bm));
                if (ex.equals(userFlag)) {
                    Toast.makeText(MainActivity.this, "Flag Good!", Toast.LENGTH_LONG).show();
                } else {
                    Toast.makeText(MainActivity.this, "Flag NOT Good...", Toast.LENGTH_LONG).show();
                }
            }
        });

    }

    private String extractTextFromImage(Bitmap bitmap) {
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();
        StringBuilder binaryText = new StringBuilder();
        int[] channels = {0, 1, 2}; // R, G, B
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int pixel = bitmap.getPixel(x, y);
                int channel = channels[binaryText.length() % 3];
                int value = (channel == 0) ? (pixel >> 16) & 0xFF : (channel == 1) ? (pixel >> 8) & 0xFF : pixel & 0xFF;
                binaryText.append(value & 1);
                if (binaryText.length() % 8 == 0 && binaryText.substring(binaryText.length() - 8).equals("00000000")) {
                    return binaryToString(binaryText.substring(0, binaryText.length() - 8));
                }
            }
        }
        return "No text founded...";
    }

    private String binaryToString(String binaryText) {
        StringBuilder text = new StringBuilder();
        for (int i = 0; i < binaryText.length(); i += 8) {
            int charCode = Integer.parseInt(binaryText.substring(i, i + 8), 2);
            text.append((char) charCode);
        }
        return text.toString();
    }


    private String decodeBase64(String encodedText) {
        try {
            byte[] decodedBytes = Base64.decode(encodedText, Base64.DEFAULT);
            return new String(decodedBytes);
        } catch (Exception e) {
            return "Base64 decode error";
        }
    }

}
