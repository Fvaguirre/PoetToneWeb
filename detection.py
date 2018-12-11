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

def doTheyRhyme ( word1, word2 ):
    # first, we don't want to report 'glue' and 'unglue' as rhyming words
    # those kind of rhymes are LAME
    if word1.find ( word2 ) == len(word1) - len ( word2 ):
        return False
    if word2.find ( word1 ) == len ( word2 ) - len ( word1 ): 
        return False

    return word1 in rhyme ( word2, 1 )

def similies(Sentence_set):
    result = []
    for sen in Sentence_set:
        sen_break = sen.split();
        if (( "like"  in sen_break) or ("as"  in sen_break)):
            result.append(sen)
    return result

def alliter(Sentence_set):
    result = []
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
                    result.append(" ".join(sen_break) )
            if(counter==1):
                last_character=ele_in[0]
            counter+=1     
    return result

def repetition(Sentence_set):
    result = []
    for sen in Sentence_set:
        sen_break = sen.split();
        if (sen_break is None or  len(sen_break) == 0 or sen_break==" "):
            continue
        for ele_in in sen_break:
            sen_break.remove(ele_in)
            if (ele_in in sen_break):
                result.append(sen +"      -word of Repetitions:"+ ele_in)    
    return result

if __name__ == "__main__":
    string = 'Let the bird of loudest lay\r\nOn the sole Arabian tree\r\nHerald sad and trumpet be,\r\nTo whose sound chaste wings obey.\r\n\r\nBut thou shrieking harbinger,\r\nFoul precurrer of the fiend,\r\nAugur of the fever\'s end,\r\nTo this troop come thou not near.\r\n\r\nFrom this session interdict\r\nEvery fowl of tyrant wing,\r\nSave the eagle, feather\'d king;\r\nKeep the obsequy so strict.\r\n\r\nLet the priest in surplice white,\r\nThat defunctive music can,\r\nBe the death-divining swan,\r\nLest the requiem lack his right.\r\n\r\nAnd thou treble-dated crow,\r\nThat thy sable gender mak\'st\r\nWith the breath thou giv\'st and tak\'st,\r\n\'Mongst our mourners shalt thou go.\r\n\r\nHere the anthem doth commence:\r\nLove and constancy is dead;\r\nPhoenix and the Turtle fled\r\nIn a mutual flame from hence.\r\n\r\nSo they lov\'d, as love in twain\r\nHad the essence but in one;\r\nTwo distincts, division none:\r\nNumber there in love was slain.\r\n\r\nHearts remote, yet not asunder;\r\nDistance and no space was seen\r\n\'Twixt this Turtle and his queen:\r\nBut in them it were a wonder.\r\n\r\nSo between them love did shine\r\nThat the Turtle saw his right\r\nFlaming in the Phoenix\' sight:\r\nEither was the other\'s mine.\r\n\r\nProperty was thus appalled\r\nThat the self was not the same;\r\nSingle nature\'s double name\r\nNeither two nor one was called.\r\n\r\nReason, in itself confounded,\r\nSaw division grow together,\r\nTo themselves yet either neither,\r\nSimple were so well compounded;\r\n\r\nThat it cried, "How true a twain\r\nSeemeth this concordant one!\r\nLove has reason, reason none,\r\nIf what parts can so remain."\r\n\r\nWhereupon it made this threne\r\nTo the Phoenix and the Dove,\r\nCo-supremes and stars of love,\r\nAs chorus to their tragic scene:\r\n\r\n                 threnos\r\n\r\nBeauty, truth, and rarity,\r\nGrace in all simplicity,\r\nHere enclos\'d, in cinders lie.\r\n\r\nDeath is now the Phoenix\' nest,\r\nAnd the Turtle\'s loyal breast\r\nTo eternity doth rest,\r\n\r\nLeaving no posterity:\r\n\'Twas not their infirmity,\r\nIt was married chastity.\r\n\r\nTruth may seem but cannot be;\r\nBeauty brag but \'tis not she;\r\nTruth and beauty buried be.\r\n\r\nTo this urn let those repair\r\nThat are either true or fair;\r\nFor these dead birds sigh a prayer.'
    
    lin = string.replace(","," ").replace("."," ")\
        .replace(";"," ").replace(":"," ").replace("!"," ")
    line = lin.splitlines()
    Set=[]
    Sentence_set=[]
    result=""
    
    for li in line:
        #print(li)
        Sentence_set.append(li)
        sp=li.split()
        if ("".join(sp[-1:]) is None or  len("".join(sp[-1:])) == 0 or "".join(sp[-1:])==" "):
            continue
        #print (str(i)+" "+"".join(sp[-1:]))
        Set.append("".join(sp[-1:]) )
        if(len(Set)%4==0):
            if(  doTheyRhyme(Set[len(Set)-4], Set[len(Set)-3] )==True and  doTheyRhyme(Set[len(Set)-3], Set[len(Set)-2] )==True and doTheyRhyme(Set[len(Set)-2], Set[len(Set)-1] )==True):
                result= ("--AAAA--")
            elif (  doTheyRhyme(Set[len(Set)-4], Set[len(Set)-3] )==True and  doTheyRhyme(Set[len(Set)-3], Set[len(Set)-2] )==False and doTheyRhyme(Set[len(Set)-2], Set[len(Set)-1] )==True):
                result =("--AABB--")
            elif (  doTheyRhyme(Set[len(Set)-4], Set[len(Set)-2] )==True and  doTheyRhyme(Set[len(Set)-3], Set[len(Set)-1] )==False and doTheyRhyme(Set[len(Set)-3], Set[len(Set)-2] )==False):
                result =("--ABAB--")
            elif (  doTheyRhyme(Set[len(Set)-4], Set[len(Set)-1] )==True and  doTheyRhyme(Set[len(Set)-3], Set[len(Set)-1] )==False and doTheyRhyme(Set[len(Set)-3], Set[len(Set)-2] )==True):
                result =("--ABBA--")
    if(result==""):    
        result= ("--No Rhyme--")
        
    print ("---last word of the sentence, see the below for the result ---")
    print(result)           
   
    print ("--sentences for similes  in first poem--")
    print (similies(Sentence_set)) 
   
    print ("--sentences for alliterations  in first poem--")
    print (alliter(Sentence_set))  
   
    print ("--sentences for repetitions   in first poem--")
    print (repetition(Sentence_set))
                
