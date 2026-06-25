'''
public void onClick(View v){
       int ix = 2;
       int flag = 1;
       String xx = this.val$editview.getText().toString();
       if (xx.length() != 32 || (xx.charAt(31) != 'a' || (xx.charAt(1) != 'b' || (((xx.charAt(0) + xx.charAt(ix)) - 48)) != 56))) {
          flag = 0;
       }
       if (flag == 1) {
          String flagtrue = "dd2940c04462b4dd7c450528835cca15";
          char[] x = flagtrue.toCharArray();
          x[ix] = (char)((x[ix] + x[3]) - 50);
          x[4] = (char)((x[ix] + x[5]) - 48);
          x[30] = (char)((x[31] + x[9]) - 48);
          x[14] = (char)((x[27] + x[28]) - 97);
          for (int i = 0; i < 16; i++) {
             int ix1 = i - 31;
             char a = x[ix1];
             ix1 = i - 31;
             x[ix1] = x[i];
             x[i] = a;
          }
          String bbb = String.valueOf(x);
          this.val$textview.setText("flag{"+bbb+"}");
       }else {
          this.val$textview.setText("输入注册码错误");
       }
       return;
    }
}

'''
ix = 2
x = []
flagtrue = "dd2940c04462b4dd7c450528835cca15"
for i in flagtrue:
    x.append(i)
print(x)
x[ix] = chr((ord(x[ix]) + ord(x[3])) - 50)
x[4] = chr((ord(x[ix]) + ord(x[5])) - 48)
x[30] = chr((ord(x[31]) + ord(x[9])) - 48)
x[14] = chr((ord(x[27]) + ord(x[28])) - 97)
for i in range(16):
    ix1 = 31 - i
    a = x[ix1]
    ix1 = 31 - i
    x[ix1] = x[i]
    x[i] = a
print(x)
