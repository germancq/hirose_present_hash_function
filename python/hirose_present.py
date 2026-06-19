# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    hirose_present.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: germancq <germancq@dte.us.es>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/11 10:39:41 by germancq          #+#    #+#              #
#    Updated: 2019/10/17 16:08:13 by germancq         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import importlib
import sys
sys.path.append('/home/germancq/gitProjects/IPCores/block_ciphers/present_cipher/python_code')
import present
import math
import numpy



class HirosePresent :
    
    def __init__(self,c,len_value):
        self.c = c 
        self.len_value = len_value
        self.present_right = present.Present(0x00000000000000000000)
        self.present_left  = present.Present(0x00000000000000000000)

    def generate_hash(self,plaintext) :
        #key in Present is 80 bits
        # the key iterates is the concatenation of right present with 16 bits of plaintext

        hr_prev = 0x0000000000000000
        hl_prev = 0x0000000000000000
        
        i = 0

        if(self.len_value == 0) :
            #print(numpy.log2(plaintext))
            i = math.ceil(math.log2(plaintext)/16)
            #print(i)
        else :
            i = math.ceil(self.len_value/16)   
        
        while i > 0 :
            #print("////////////////////////////////")
            #print(i)
            i = i - 1
            #print(hex(plaintext))
            m_i = plaintext & 0xFFFF
            plaintext = plaintext >> 16
            key_i = (hr_prev << 16) | m_i
            #print(hex(m_i))
            #print(hex(key_i))
            #print(hex(hl_prev))
            #print(hex(hr_prev))

            self.present_right.refresh_key(key_i)
            self.present_left.refresh_key(key_i)

            plaintext_right = self.c ^ hl_prev
            #print(hex(plaintext_right))
            hr_i = self.present_right.encrypt(plaintext_right)
            #print(hex(hr_i))
            hr_prev = hr_i ^ plaintext_right

            plaintext_left = hl_prev
            hl_i = self.present_left.encrypt(plaintext_left)
            #print(hex(hl_i))
            hl_prev = hl_i ^ plaintext_left
            #print("///////////////////////////////////////")


        #print("////////////////////////////////----------------")
        #print(hex(hl_prev))
        #print(hex(hr_prev))
        return ((hl_prev<<64) | hr_prev)
      



if __name__ == "__main__":
    hirose_present_hash_impl = HirosePresent(0x1234567812345678,64)
    text = 0x4b6fa49c
    hash_value = hirose_present_hash_impl.generate_hash(text)
    #print(hex(hash_value))