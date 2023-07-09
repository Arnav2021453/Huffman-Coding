import os
import heapq
class BinaryTreeNode:
    def __init__(self,value,freq):
        self.value=value
        self.freq=freq
        self.left=None
        self.right=None
    def __lt__(self,other):
        return self.freq<other.freq
    def __eq__(self,other):
        return self.freq==other.freq        
class HuffmanCoding:
    def __init__(self,path):
        self.path=path
        self.__heap=[]
        self.__codes={}
        self.__reversecodes={}
    def __makefreqdict(self,text):
        freq_dict={}
        for char in text:
            if char not in freq_dict:
                freq_dict[char]=0
            freq_dict[char]+=1
        return freq_dict
    def __buildheap(self,freq_dict):
        for key in freq_dict:
            frequency=freq_dict[key]
            btn=BinaryTreeNode(key,frequency)
            heapq.heappush(self.__heap,btn)
    def __buildtree(self):
        while len(self.__heap)>1:
            btn1=heapq.heappop(self.__heap)
            btn2=heapq.heappop(self.__heap)
            freqs=btn1.freq+btn2.freq
            newnode=BinaryTreeNode(None,freqs)
            newnode.left=btn1
            newnode.right=btn2
            heapq.heappush(self.__heap,newnode)
        return   
    def __buildcodeshelper(self,root,curr_bits):
        if root is None:
            return
        if root.value is not None:
            self.__codes[root.value]=curr_bits
            self.__reversecodes[curr_bits]=root.value
            return
        self.__buildcodeshelper(root.left, curr_bits+"0")
        self.__buildcodeshelper(root.right, curr_bits+"1")
    def __buildcodes(self):
        root=heapq.heappop(self.__heap)
        self.__buildcodeshelper(root,'')
    def __encodingtext(self,text):
        encodedtext=''
        for char in text:
            encodedtext+=self.__codes[char]
        return encodedtext  
    def __pad(self,encoded_text):
        padamt=8-(len(encoded_text)%8)
        for i in range(padamt):
            encoded_text+='0'
        padinfo="{0:08b}".format(padamt)
        padded_encoded_text=padinfo+encoded_text
        return padded_encoded_text
    def __getbytesarray(self,padded_encoded_text):
        arr=[]
        for i in range(0,len(padded_encoded_text),8):
            byte=padded_encoded_text[i:i+8]
            arr.append(int(byte,2))
        return arr    
    def compress(self):
        file_name,file_extension=os.path.splitext(self.path)
        output_path=file_name+".bin"
        with open(self.path,'r+') as file,open(output_path,'wb') as output:
            text=file.read()
            text=text.rstrip()
            freq_dict=self.__makefreqdict(text)
            self.__buildheap(freq_dict)
            self.__buildtree()
            self.__buildcodes()
            encoded_text=self.__encodingtext(text)
            padded_encoded_text=self.__pad(encoded_text)
            bytesarray=self.__getbytesarray(padded_encoded_text)
            finalbytes=bytes(bytesarray)
            output.write(finalbytes)
        print("Compressed")
        return output_path    
    def __removepad(self,text):
        padinfo=text[:8]
        extrapadding=int(padinfo,2)
        text=text[8:]
        finaltext=text[:(-1)*extrapadding]
        return finaltext
    def __decodetext(self,text):
        decodedtext=''
        currentbits=''
        for bit in text:
            currentbits+=bit
            if currentbits in self.__reversecodes:
                char=self.__reversecodes[currentbits]
                decodedtext+=char
                currentbits=''
        return decodedtext            
    def decompress(self,input_path):
        filename,fileextension=os.path.splitext(self.path)
        outputpath=filename+"_decompressed"+".txt"
        with open(input_path,'rb') as file,open(outputpath,'w') as output:
            bitstring=''
            byte=file.read(1)
            while byte:
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bitstring+=bits
                byte=file.read(1)
            actualtext=self.__removepad(bitstring)        
            decompressedtext=self.__decodetext(actualtext)
            output.write(decompressedtext)
        print("Decompressed")   
        return 
path="C:/Users/dell/OneDrive/Desktop/sample.txt"
h=HuffmanCoding(path)
output_path=h.compress()
h.decompress(output_path)