# Reverse.class (Java) reversing
'''
public static void Encrypt(char arr[])
	{
		ArrayList Resultlist = new ArrayList();
		for (int i = 0; i < arr.length; i++)     计算加密
		{
			int result = arr[i] + 64 ^ 0x20;
			Resultlist.add(Integer.valueOf(result));
		}

		int KEY[] = {                            准备对照的flag
			180, 136, 137, 147, 191, 137, 147, 191, 148, 136,
			133, 191, 134, 140, 129, 135, 191, 65
		};
		ArrayList KEYList = new ArrayList();
		for (int j = 0; j < KEY.length; j++)
			KEYList.add(Integer.valueOf(KEY[j]));

		System.out.println("Result:");
		if (Resultlist.equals(KEYList))
			System.out.println("Congratulations！");
		else
			System.err.println("Error！");
	}

'''
KEY = [180, 136, 137, 147, 191, 137, 147, 191, 148, 136, 133, 191, 134, 140, 129, 135, 191, 65]
flag = ''.join(chr((k ^ 32) - 64) for k in KEY)
print("\nFLAG = flag{%s}" % flag)
