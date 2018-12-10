import numpy as np
import pandas as pd
import nltk

def rhyme(inp, level):
     entries = nltk.corpus.cmudict.entries()
     syllables = [(word, syl) for word, syl in entries if word == inp]
     rhymes = []
     for (word, syllable) in syllables:
          rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
     return set(rhymes)

def doTheyRhyme(word1, word2):
     if word1.find(word2) == len(word1) - len(word2):
          return False
     if word2.find(word1) == len(word2) - len(word1): 
          return False

     return word1 in rhyme(word2, 1)

def evaluate(istr):
     istr = istr.replace(","," ").replace("."," ").replace(";"," ").replace(":"," ").replace("!"," ")
     line = istr.splitlines()
     i=0
     Set = []
     S_set = []
     result = ""
     for li in line:
          S_set.append(li)
          sp = li.split()
          print(sp)
          if("".join(sp[-1:]) is None or len("".join(sp[-1:])) == 0 or "".join(sp[-1:])==" "):
               continue
          print (str(i)+" "+"".join(sp[-1:]))
          Set.append("".join(sp[-1:]))
          if(len(Set)%4==0):
               if(  doTheyRhyme(Set[len(Set)-4], Set[len(Set)-3] )==True and  doTheyRhyme(Set[len(Set)-3], Set[len(Set)-2] )==True and doTheyRhyme(Set[len(Set)-2], Set[len(Set)-1] )==True):
                    result = "--AAAA--"
               elif(doTheyRhyme(Set[len(Set)-4], Set[len(Set)-3] )==True and  doTheyRhyme(Set[len(Set)-3], Set[len(Set)-2] )==False and doTheyRhyme(Set[len(Set)-2], Set[len(Set)-1] )==True):
                    result = "--AABB--"
               elif (  doTheyRhyme(Set[len(Set)-4], Set[len(Set)-2] )==True and  doTheyRhyme(Set[len(Set)-3], Set[len(Set)-1] )==False and doTheyRhyme(Set[len(Set)-3], Set[len(Set)-2] )==False):
                    result = "--ABAB--"
               elif (  doTheyRhyme(Set[len(Set)-4], Set[len(Set)-1] )==True and  doTheyRhyme(Set[len(Set)-3], Set[len(Set)-1] )==False and doTheyRhyme(Set[len(Set)-3], Set[len(Set)-2] )==True):
                    result = "--ABBA--"   
          i=i+1
     if(result==""):
          result=("--No Rhyme--")
     print(result)
     print ("--sentences for similes  in first poem--")
     for sen in Sentence_set:
          sen_break = sen.split();
          if (( "like"  in sen_break) or ("as"  in sen_break)):
               print (sen)  
     
     print ("--sentences for alliterations  in first poem--")
     for sen in Sentence_set:
          sen_break = sen.split();
          if (sen_break is None or  len(sen_break) == 0 or sen_break==" "):
               continue
          counter=1
          threeorfour=1
          last_character=''
          for ele_in in sen_break:
               if (ele_in[0]==last_character):
                    threeorfour+=1
                    if(counter==3):
                         print (" ".join(sen_break) )
               if(counter==1):
                    last_character=ele_in[0]
               counter+=1
     
     print ("--sentences for repetitions   in first poem--")
     for sen in Sentence_set:
          sen_break = sen.split();
          if (sen_break is None or  len(sen_break) == 0 or sen_break==" "):
               continue
          for ele_in in sen_break:
               sen_break.remove(ele_in)
               if (ele_in in sen_break):
                    print (sen +"      -word of Repetitions:"+ ele_in)     


     
     print(S_set)
     return

if __name__ == "__main__":
     inputstr = str(input("Enter string: "))
     print(evaluate(inputstr))