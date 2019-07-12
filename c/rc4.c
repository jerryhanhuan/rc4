#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>


void swap(unsigned char *s1,unsigned char *s2)
{
	unsigned char temp;
	temp = *s1;
	*s1 = *s2;
	*s2 = temp;
}



int rc4_encrypt(unsigned char *key,int keylen,unsigned char *data,int datalen,unsigned char *out)
{
	unsigned char S[256]={0};
	unsigned char T[256]={0};
	// 初始化S,按照升序,给每个字节赋值 0,1,2,3,4,5....,254,255
	int i,j = 0;
	for (i=0;i<256;i++)
	{
		S[i]=i;
		T[i]=key[i%keylen];
	}
	//利用Key生成S盒——The key-scheduling algorithm (KSA)
	//初始化密钥,密钥长度[1,256] 
	//这样处理的状态向量S就带有一定的随机性了
	for (i=0;i<256;i++)
	{
		j = (j+S[i]+T[i])%256;
		swap(&S[i],&S[j]);
	}
	//利用S盒生成密钥流——The pseudo-random generation algorithm(PRGA)
	i = 0;
	j = 0;
	unsigned char k = 0;
	int m= 0;
	while(datalen--)
	{
		i = (i+1)%256;
		j = (j+S[i])%256;
		swap(&S[i],&S[j]);
		k = S[(S[i]+S[j])%256];
		out[m]=k^data[m];
		m++;
	}

}

static void printHex(unsigned char* data,int datalen)
{
	int i = 0;
	for(i=0;i<datalen;i++)
		printf("%02X",data[i]);
	printf("\n");
}

int main(int argc,char **argv)
{
	if(argc<3)
	{
		printf("Usage key data");
		return -1;
	}
	unsigned char key[256]={0};
	unsigned char data[8192]={0};
	unsigned char out[8192]={0};
	memcpy(key,argv[1],strlen(argv[1]));
	int keylen = strlen(argv[1]);
	int len =  strlen(argv[2]);
	memcpy(data,argv[2],len);
	int ret = rc4_encrypt(key,keylen,data,len,out);

	printf("cryptlen:[%d] .\n",ret);
	printHex(out,ret);

	unsigned char plain[8192]={0};
	ret = rc4_encrypt(key,keylen,out,len,plain);
	printf("plain::%s.\n",plain);
	return 0;
}

