import os
import requests
import tarfile
import re
import glob
import shutil
if 64 - 64: i11iIiiIii
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
class ruleManager:
 def __init__ ( self , fm , gm , cp , rp ) :
  print ( "Initializing Rule Manager." )
  self . fm = fm
  self . gm = gm
  self . cp = cp
  self . rp = rp
  if 78 - 78: i11i . oOooOoO0Oo0O
 def build ( self ) :
  self . clearTmp ( )
  self . initTmp ( )
  self . gitPull ( )
  self . initReports ( )
  self . migrateOldRules ( )
  self . getNewRules ( )
  self . extract ( )
  self . mergeCategories ( )
  self . purgeOld ( )
  self . etDisables ( )
  self . updateRuleState ( )
  self . applyCustomDisables ( )
  self . moveRules ( )
  self . callReporter ( )
  self . gitPush ( )
  if 10 - 10: IIiI1I11i11
 def clearTmp ( self ) :
  print ( "Clearing Temp directories." )
  ooOO00oOo = self . cp . getSystemConfig ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  self . fm . clearDir ( OOOo0 , True )
  if 54 - 54: i1 - o0 * i1oOo0OoO * iIIIiiIIiiiIi % Oo
  if 67 - 67: O00ooOO . I1iII1iiII
 def initTmp ( self ) :
  print ( "Re-initializing Temp directories." )
  ooOO00oOo = self . cp . getSystemConfig ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  self . fm . createDir ( ( OOOo0 + "/rules" ) )
  self . fm . createDir ( ( OOOo0 + "/rules-new" ) )
  self . fm . createDir ( ( OOOo0 + "/rules-old" ) )
  if 28 - 28: Ii11111i * iiI1i1
 def gitPull ( self ) :
  print ( "Performing git Pull." )
  ooOO00oOo = self . cp . getSystemConfig ( )
  i1I1ii1II1iII = ooOO00oOo [ "git-dir" ]
  self . gm . pull ( i1I1ii1II1iII )
  if 86 - 86: oO0o
 def initReports ( self ) :
  print ( "Initializing reports directory." )
  ooOO00oOo = self . cp . getSystemConfig ( )
  i1I1ii1II1iII = ooOO00oOo [ "git-dir" ]
  if 12 - 12: OOO0o0o / o0oO0 + O0 * i11i / oO0o * oO0o
  if not os . path . isdir ( ( i1I1ii1II1iII + "/reports" ) ) :
   self . fm . createDir ( ( i1I1ii1II1iII + "/reports" ) )
   if 37 - 37: iiI1i1
 def migrateOldRules ( self ) :
  ooOO00oOo = self . cp . getSystemConfig ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  i1I1ii1II1iII = ooOO00oOo [ "git-dir" ]
  print ( "Moving old rules to " + OOOo0 + "/rules-old/all.rules." )
  if os . path . isfile ( ( i1I1ii1II1iII + "/all.rules" ) ) :
   self . fm . mvFile ( ( i1I1ii1II1iII + "/all.rules" ) , ( OOOo0 + "/rules-old/all.rules" ) )
  if os . path . isfile ( ( i1I1ii1II1iII + "/local.rules" ) ) :
   self . fm . mvFile ( ( i1I1ii1II1iII + "/local.rules" ) , ( OOOo0 + "/rules-old/local.rules" ) )
   if 71 - 71: O00ooOO * iiI1i1 . O00ooOO / OOO0o0o
   if 14 - 14: iIii1I11I1II1
 def getNewRules ( self ) :
  print ( "Retrieving new rules." )
  o0oOoO00o = self . cp . getRuleUrl ( )
  i1oOOoo00O0O = o0oOoO00o [ "rule-url" ]
  ooOO00oOo = self . cp . getSystemConfig ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  #gitDir = sysConfig["git-dir"]
  if 15 - 15: oOooOoO0Oo0O
  if 90 - 90: oO0o * i1IIi / Ii11111i . i1 * Oo
  I111i1i1111i = requests . get ( i1oOOoo00O0O , stream = True )
  o0o0Oo0oooo0 = open ( ( OOOo0 + "/rules.tar.gz" ) , "wb" )
  for oO0O0o0o0 in I111i1i1111i . iter_content ( chunk_size = 1024 ) :
   if oO0O0o0o0 :
    o0o0Oo0oooo0 . write ( oO0O0o0o0 )
    o0o0Oo0oooo0 . flush ( )
  o0o0Oo0oooo0 . close ( )
  if 27 - 27: i1
 def extract ( self ) :
  print ( "Extracting rules from tarball." )
  ooOO00oOo = self . cp . getSystemConfig ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  if 73 - 73: i1oOo0OoO - IIiI1I11i11
  o0o0Oo0oooo0 = tarfile . open ( ( OOOo0 + "/rules.tar.gz" ) , "r:gz" )
  o0o0Oo0oooo0 . extractall ( path = OOOo0 + "/rules/" )
  o0o0Oo0oooo0 . close ( )
  if 58 - 58: i11iIiiIii % OOO0o0o
  if 54 - 54: O00ooOO % O0 + oOooOoO0Oo0O - iiI1i1 / I1iII1iiII
 def mergeCategories ( self ) :
  print ( "Merging categories into a new all.rules file." )
  ooOO00oOo = self . cp . getSystemConfig ( )
  iIiiI1 = self . cp . getCategories ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  if 68 - 68: oOooOoO0Oo0O - i11iIiiIii - i1 / O00ooOO - i1 + i1IIi
  if 48 - 48: OoooooooOO % i1oOo0OoO . oOooOoO0Oo0O - Ii11111i % i1IIi % OoooooooOO
  if 3 - 3: iiI1i1 + O0
  o0o0Oo0oooo0 = open ( ( OOOo0 + "/rules-new/all.rules-new" ) , "w" )
  if 42 - 42: O00ooOO / i1IIi + i11iIiiIii - Ii11111i
  for oo0Ooo0 in iIiiI1 :
   if ( os . path . isfile ( ( OOOo0 + "/rules/rules/" + oo0Ooo0 ) ) ) :
    I1I11I1I1I = open ( ( OOOo0 + "/rules/rules/" + oo0Ooo0 ) , "r" )
    for OooO0OO in I1I11I1I1I :
     o0o0Oo0oooo0 . write ( OooO0OO )
    I1I11I1I1I . close ( )
   else :
    print ( "ALERT: Category: " + oo0Ooo0 + " does not exist. Rules will not be added. Please check mob-boss.yaml and disable " + oo0Ooo0 + "." )
  print ( "Rule merge complete." )
  o0o0Oo0oooo0 . close ( )
  if 28 - 28: i11i
  if 28 - 28: iIii1I11I1II1 - i1IIi
 def purgeOld ( self ) :
  print ( "Purging old rules from rule_state.conf. This may take a bit." )
  ooOO00oOo = self . cp . getSystemConfig ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  i1I1ii1II1iII = ooOO00oOo [ "git-dir" ]
  OO = [ ]
  oO0O = [ ]
  OOoO000O0OO = [ ]
  if 23 - 23: i11iIiiIii + oOooOoO0Oo0O
  if os . path . isfile ( i1I1ii1II1iII + "/rule_state.conf" ) :
   o0o0Oo0oooo0 = open ( ( i1I1ii1II1iII + "/rule_state.conf" ) , "r" )
  else :
   o0o0Oo0oooo0 = open ( ( i1I1ii1II1iII + "/rule_state.conf" ) , "w" )
   o0o0Oo0oooo0 . write ( "sid,state,name\n" )
   o0o0Oo0oooo0 . close ( )
   o0o0Oo0oooo0 = open ( ( i1I1ii1II1iII + "/rule_state.conf" ) , "r" )
   if 68 - 68: o0 . Oo . i11iIiiIii
  for OooO0OO in o0o0Oo0oooo0 :
   OO . append ( OooO0OO )
  o0o0Oo0oooo0 . close ( )
  if 40 - 40: Oo . o0 . IIiI1I11i11 . i1IIi
  I11iii = 0
  while I11iii < len ( OO ) :
   OO [ I11iii ] = OO [ I11iii ] . split ( "," )
   I11iii = I11iii + 1
   if 54 - 54: O00ooOO + O00ooOO % OOO0o0o % i11iIiiIii / iIii1I11I1II1 . O00ooOO
  o0o0Oo0oooo0 = open ( ( OOOo0 + "/rules-new/all.rules-new" ) , "r" )
  for OooO0OO in o0o0Oo0oooo0 :
   oO0O . append ( OooO0OO )
  o0o0Oo0oooo0 . close ( )
  o0oO0o00oo = [ ]
  II1i1Ii11Ii11 = ""
  if 35 - 35: i1oOo0OoO + iiI1i1 + iiI1i1
  for OooO0OO in oO0O :
   if not OooO0OO == "" :
    II1i1Ii11Ii11 = re . search ( r'; sid:[0-9]*' , OooO0OO )
    if not II1i1Ii11Ii11 == None :
     II1i1Ii11Ii11 = II1i1Ii11Ii11 . group ( 0 ) . strip ( "; sid:" )
     o0oO0o00oo . append ( II1i1Ii11Ii11 )
     if 11 - 11: iiI1i1 - i1 % o0oO0 % iiI1i1 / o0 - i1
     if 74 - 74: iiI1i1 * O0
     if 89 - 89: Oo + IIiI1I11i11
  OOoO000O0OO . append ( OO [ 0 ] [ 0 ] + "," + OO [ 0 ] [ 1 ] + "," + OO [ 0 ] [ 2 ] )
  if 3 - 3: i1IIi / oOooOoO0Oo0O % I1iII1iiII * i11iIiiIii / O0 * I1iII1iiII
  if 49 - 49: Oo % Ii11111i + i1IIi . oOooOoO0Oo0O % iIIIiiIIiiiIi
  for I1i1iii in OO :
   if 20 - 20: i1oOo0OoO
   if not I1i1iii [ 0 ] == "sid" :
    if 77 - 77: o0 / I1iII1iiII
    if I1i1iii [ 0 ] in o0oO0o00oo :
     OOoO000O0OO . append ( I1i1iii [ 0 ] + "," + I1i1iii [ 1 ] + "," + I1i1iii [ 2 ] )
     if 98 - 98: iIii1I11I1II1 / i1IIi / i11iIiiIii / i1oOo0OoO
     if 28 - 28: O00ooOO - oO0o . oO0o + o0 - OoooooooOO + O0
  o0o0Oo0oooo0 = open ( ( i1I1ii1II1iII + "/rule_state.conf" ) , "w" )
  for OooO0OO in OOoO000O0OO :
   if not OooO0OO [ len ( OooO0OO ) - 1 ] == "\n" :
    OooO0OO = OooO0OO + "\n"
   o0o0Oo0oooo0 . write ( OooO0OO )
   if 95 - 95: i1 % Oo . O0
  o0o0Oo0oooo0 . close ( )
  if 15 - 15: o0oO0 / Ii11111i . Ii11111i - i1IIi
  if 53 - 53: oO0o + oOooOoO0Oo0O * Oo
 def etDisables ( self ) :
  print ( "Processing disables." )
  ooOO00oOo = self . cp . getSystemConfig ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  i1I1ii1II1iII = ooOO00oOo [ "git-dir" ]
  OO = [ ]
  o0oO0o00oo = [ ]
  if 61 - 61: i1IIi * O00ooOO / OoooooooOO . i11iIiiIii . o0
  if 60 - 60: I1iII1iiII / I1iII1iiII
  o0o0Oo0oooo0 = open ( ( i1I1ii1II1iII + "/rule_state.conf" ) , "r" )
  if 46 - 46: Ii11111i * O00ooOO - i1 * Oo - OOO0o0o
  if 83 - 83: OoooooooOO
  for OooO0OO in o0o0Oo0oooo0 :
   OO . append ( OooO0OO . split ( "," ) )
  o0o0Oo0oooo0 . close ( )
  if 31 - 31: i11i - O00ooOO . OOO0o0o % o0 - O0
  o0o0Oo0oooo0 = open ( ( OOOo0 + "/rules-new/all.rules-new" ) , "r" )
  if 4 - 4: i11i / o0oO0 . iiI1i1
  if 58 - 58: O00ooOO * i11iIiiIii / o0 % OOO0o0o - iIIIiiIIiiiIi / Oo
  for OooO0OO in o0o0Oo0oooo0 :
   if OooO0OO . find ( "#" ) == 0 :
    II1i1Ii11Ii11 = re . search ( r'; sid:[0-9]*' , OooO0OO )
    if not II1i1Ii11Ii11 == None :
     II1i1Ii11Ii11 = II1i1Ii11Ii11 . group ( 0 ) . strip ( "; sid:" )
     o0oO0o00oo . append ( II1i1Ii11Ii11 )
     if 50 - 50: oOooOoO0Oo0O
     if 34 - 34: oOooOoO0Oo0O * i11i % iiI1i1 * o0 - oOooOoO0Oo0O
  for I1i1iii in OO :
   if I1i1iii [ 0 ] in o0oO0o00oo :
    I1i1iii [ 1 ] = "0"
    if 33 - 33: i1oOo0OoO + O00ooOO * i1 - IIiI1I11i11 / Oo % Ii11111i
  o0o0Oo0oooo0 = open ( ( i1I1ii1II1iII + "/rule_state.conf" ) , "w" )
  for I1i1iii in OO :
   o0o0Oo0oooo0 . write ( I1i1iii [ 0 ] + "," + I1i1iii [ 1 ] + "," + I1i1iii [ 2 ] )
   if 21 - 21: i1 * iIii1I11I1II1 % Oo * i1IIi
  o0o0Oo0oooo0 . close ( )
  if 16 - 16: O0 - OOO0o0o * iIii1I11I1II1 + iiI1i1
  if 50 - 50: i11i - o0oO0 * iIIIiiIIiiiIi / OOO0o0o + i1oOo0OoO
  if 88 - 88: Ii11111i / OOO0o0o + iiI1i1 - i11i / o0oO0 - o0
 def updateRuleState ( self ) :
  print ( "Updating rule_state.conf with new rules." )
  ooOO00oOo = self . cp . getSystemConfig ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  i1I1ii1II1iII = ooOO00oOo [ "git-dir" ]
  OO = [ ]
  IIIIii = [ ]
  o0oO0o00oo = [ ]
  O0o0 = [ ]
  if 71 - 71: O00ooOO + o0oO0 % i11iIiiIii + iIIIiiIIiiiIi - oO0o
  o0o0Oo0oooo0 = open ( ( i1I1ii1II1iII + "/rule_state.conf" ) , "r" )
  if 88 - 88: o0 - i1 % O00ooOO
  for OooO0OO in o0o0Oo0oooo0 :
   OO . append ( OooO0OO . split ( "," ) )
  o0o0Oo0oooo0 . close ( )
  if 16 - 16: oOooOoO0Oo0O * Oo % oO0o
  II1i1Ii11Ii11 = ""
  o0o0Oo0oooo0 = open ( ( OOOo0 + "/rules-new/all.rules-new" ) , "r" )
  if 86 - 86: oOooOoO0Oo0O + Ii11111i % i11iIiiIii * Oo . o0oO0 * I1iII1iiII
  for OooO0OO in o0o0Oo0oooo0 :
   if not OooO0OO . find ( "#" ) == 0 and not OooO0OO == "" :
    II1i1Ii11Ii11 = re . search ( r'; sid:[0-9]*' , OooO0OO )
    if not II1i1Ii11Ii11 == None :
     II1i1Ii11Ii11 = II1i1Ii11Ii11 . group ( 0 ) . strip ( "; sid:" )
     o0oO0o00oo . append ( II1i1Ii11Ii11 )
  o0o0Oo0oooo0 . close ( )
  if 44 - 44: Oo
  for I1i1iii in OO :
   IIIIii . append ( I1i1iii [ 0 ] )
   if 88 - 88: OOO0o0o % Ii11111i . i11i
   if 38 - 38: i1oOo0OoO
  for I1i1iii in o0oO0o00oo :
   if I1i1iii not in IIIIii :
    O0o0 . append ( I1i1iii )
    if 57 - 57: O0 / Oo * OOO0o0o / o0 . i11i
  o0o0Oo0oooo0 = open ( ( OOOo0 + "/rules-new/all.rules-new" ) , "r" )
  II1i1Ii11Ii11 = ""
  i11iIIIIIi1 = ""
  if 20 - 20: i1IIi + iIIIiiIIiiiIi - o0oO0
  if 30 - 30: i11i - O00ooOO - i11iIiiIii % o0 - i11i * Ii11111i
  for I1i1iii in O0o0 :
   if 61 - 61: Oo - I1iII1iiII % O00ooOO
   for OooO0OO in o0o0Oo0oooo0 :
    if 84 - 84: Oo * i1 / I1iII1iiII - O0
    if not OooO0OO . find ( "#" ) == 0 :
     if 30 - 30: iIii1I11I1II1 / o0oO0 - OOO0o0o - i11i % iiI1i1
     IIi1i11111 = "; sid:" + I1i1iii
     II1i1Ii11Ii11 = re . search ( IIi1i11111 , OooO0OO )
     if 81 - 81: i11iIiiIii % o0 - O00ooOO
     if not II1i1Ii11Ii11 == None :
      if 68 - 68: OOO0o0o % i1IIi . oO0o . iIIIiiIIiiiIi
      IIi1i11111 = "\(msg:\"[A-Za-z0-9 \.\-\_\(\\)\|\/\+\,\?\=]*\";"
      i11iIIIIIi1 = re . search ( IIi1i11111 , OooO0OO )
      if 92 - 92: iiI1i1 . OOO0o0o
      if not i11iIIIIIi1 == None :
       if 31 - 31: OOO0o0o . o0 / O0
       i11iIIIIIi1 = i11iIIIIIi1 . group ( 0 ) . lstrip ( "(msg:\"" ) . rstrip ( "\";" ) . replace ( "," , "" ) . replace ( "\"" , "" )
       if "," in i11iIIIIIi1 :
        print ( i11iIIIIIi1 )
       i11iIIIIIi1 = i11iIIIIIi1 + "\n"
       o000O0o = [ I1i1iii , "1" , i11iIIIIIi1 ]
       OO . append ( o000O0o )
       if 42 - 42: o0
  o0o0Oo0oooo0 . close ( )
  if 41 - 41: IIiI1I11i11 . o0oO0 + O0 * i1oOo0OoO % IIiI1I11i11 * IIiI1I11i11
  o0o0Oo0oooo0 = open ( ( i1I1ii1II1iII + "/rule_state.conf" ) , "w" )
  if 19 - 19: iiI1i1
  for I1i1iii in OO :
   o0o0Oo0oooo0 . write ( I1i1iii [ 0 ] + "," + I1i1iii [ 1 ] + "," + I1i1iii [ 2 ] )
  o0o0Oo0oooo0 . close ( )
  if 46 - 46: iIIIiiIIiiiIi - Ii11111i . iIii1I11I1II1 / iIIIiiIIiiiIi
  if 7 - 7: i1IIi / oOooOoO0Oo0O * OOO0o0o . oO0o . iIii1I11I1II1
  if 13 - 13: O00ooOO / i11iIiiIii
  if 2 - 2: oOooOoO0Oo0O / O0 / i1oOo0OoO % o0 % Ii11111i
  if 52 - 52: i1oOo0OoO
 def applyCustomDisables ( self ) :
  print ( "Applying Custom Disables." )
  ooOO00oOo = self . cp . getSystemConfig ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  i1I1ii1II1iII = ooOO00oOo [ "git-dir" ]
  o0OO0oOO0O0 = [ ]
  oO0O = [ ]
  iiiIIi1II = [ ]
  if 61 - 61: I1iII1iiII
  o0o0Oo0oooo0 = open ( ( i1I1ii1II1iII + "/rule_state.conf" ) , "r" )
  if 86 - 86: I1iII1iiII % o0 / oOooOoO0Oo0O / o0
  for OooO0OO in o0o0Oo0oooo0 :
   o0OO0oOO0O0 . append ( OooO0OO . split ( "," ) )
  o0o0Oo0oooo0 . close ( )
  if 42 - 42: i1
  if 67 - 67: OOO0o0o . iiI1i1 . O0
  o0o0Oo0oooo0 = open ( ( OOOo0 + "/rules-new/all.rules-new" ) , "r" )
  for OooO0OO in o0o0Oo0oooo0 :
   oO0O . append ( OooO0OO )
  o0o0Oo0oooo0 . close ( )
  if 10 - 10: iIIIiiIIiiiIi % iIIIiiIIiiiIi - iIii1I11I1II1 / O00ooOO + Ii11111i
  if 87 - 87: Oo * iIIIiiIIiiiIi + O00ooOO / iIii1I11I1II1 / iiI1i1
  II1i1Ii11Ii11 = ""
  if 37 - 37: iiI1i1 - o0oO0 * Oo % i11iIiiIii - OOO0o0o
  for I1i1iii in oO0O :
   if 83 - 83: I1iII1iiII / oOooOoO0Oo0O
   if not I1i1iii . find ( "#" ) == 0 :
    if 34 - 34: oO0o
    IIi1i11111 = "; sid:[0-9]*;"
    II1i1Ii11Ii11 = re . search ( IIi1i11111 , I1i1iii )
    if 57 - 57: Oo . I1iII1iiII . i1IIi
    if not II1i1Ii11Ii11 == None :
     iiiIIi1II . append ( [ II1i1Ii11Ii11 . group ( 0 ) . lstrip ( "; sid:" ) . rstrip ( ";" ) , "1" ] )
     if 42 - 42: I1iII1iiII + iIIIiiIIiiiIi % O0
  for I1i1iii in o0OO0oOO0O0 :
   if 6 - 6: Oo
   if I1i1iii [ 1 ] == "0" :
    if 68 - 68: o0 - i1
    I11iii = 0
    while I11iii < len ( iiiIIi1II ) :
     if 28 - 28: i1 . O00ooOO / O00ooOO + IIiI1I11i11 . iIIIiiIIiiiIi
     if iiiIIi1II [ I11iii ] [ 0 ] == I1i1iii [ 0 ] :
      iiiIIi1II [ I11iii ] [ 1 ] = "0"
     I11iii = I11iii + 1
     if 1 - 1: iIii1I11I1II1 / i11i
  II1i1Ii11Ii11 = ""
  if 33 - 33: I1iII1iiII
  for I1i1iii in iiiIIi1II :
   if 18 - 18: i1oOo0OoO % iiI1i1 * O0
   if I1i1iii [ 1 ] == "0" :
    if 87 - 87: i11iIiiIii
    I11iii = 0
    while I11iii < len ( oO0O ) :
     if 93 - 93: iIIIiiIIiiiIi - i1 % i11iIiiIii . iiI1i1 / iiI1i1 - OOO0o0o
     if not oO0O [ I11iii ] . find ( "#" ) == 0 :
      if 9 - 9: iIIIiiIIiiiIi / IIiI1I11i11 - oOooOoO0Oo0O / OoooooooOO / iIii1I11I1II1 - i1oOo0OoO
      IIi1i11111 = "; sid:[0-9]*;"
      II1i1Ii11Ii11 = re . search ( IIi1i11111 , oO0O [ I11iii ] )
      if 91 - 91: iiI1i1 % i1IIi % iIii1I11I1II1
      if not II1i1Ii11Ii11 == None :
       II1i1Ii11Ii11 = II1i1Ii11Ii11 . group ( 0 ) . lstrip ( "; sid:" ) . rstrip ( ";" )
       if II1i1Ii11Ii11 == I1i1iii [ 0 ] :
        oO0O [ I11iii ] = "#" + oO0O [ I11iii ]
     I11iii = I11iii + 1
     if 20 - 20: O00ooOO % Ii11111i / Ii11111i + Ii11111i
  o0o0Oo0oooo0 = open ( ( OOOo0 + "/rules-new/all.rules-new" ) , "w" )
  if 45 - 45: Oo - oO0o - OoooooooOO - i1 . i11i / O0
  for OooO0OO in oO0O :
   o0o0Oo0oooo0 . write ( OooO0OO )
   if 51 - 51: O0 + iiI1i1
  o0o0Oo0oooo0 . close ( )
  if 8 - 8: Oo * o0 - Ii11111i - i1 * O00ooOO % oOooOoO0Oo0O
  if 48 - 48: O0
  if 11 - 11: I1iII1iiII + OoooooooOO - i1 / i1oOo0OoO + IIiI1I11i11 . i11i
  if 41 - 41: Ii11111i - O0 - O0
  if 68 - 68: O00ooOO % OOO0o0o
 def moveRules ( self ) :
  ooOO00oOo = self . cp . getSystemConfig ( )
  OOOo0 = ooOO00oOo [ "temp-dir" ]
  i1I1ii1II1iII = ooOO00oOo [ "git-dir" ]
  if 88 - 88: iIii1I11I1II1 - o0oO0 + O00ooOO
  os . rename ( ( OOOo0 + "/rules-new/all.rules-new" ) , ( OOOo0 + "/rules-new/all.rules" ) )
  self . fm . mvFile ( ( i1I1ii1II1iII + "/all.rules" ) , ( OOOo0 + "/rules-old/all.rules" ) )
  self . fm . cpFile ( ( OOOo0 + "/rules-new/all.rules" ) , ( i1I1ii1II1iII + "/all.rules" ) )
  if 40 - 40: oOooOoO0Oo0O * Ii11111i + O00ooOO % iiI1i1
  for file in glob . glob ( OOOo0 + "/rules/rules/*.map" ) :
   shutil . copy ( file , ( i1I1ii1II1iII + "/" ) )
   if 74 - 74: Oo - IIiI1I11i11 + OoooooooOO + OOO0o0o / o0
  for file in glob . glob ( OOOo0 + "/rules/rules/*.config" ) :
   shutil . copy ( file , ( i1I1ii1II1iII + "/" ) )
   if 23 - 23: O0
   if 85 - 85: Ii11111i
 def callReporter ( self ) :
  self . rp . generateReport ( )
  if 84 - 84: oOooOoO0Oo0O . iIii1I11I1II1 % OoooooooOO + Ii11111i % OoooooooOO % i1
 def gitPush ( self ) :
  ooOO00oOo = self . cp . getSystemConfig ( )
  i1I1ii1II1iII = ooOO00oOo [ "git-dir" ]
  if not os . path . isfile ( ( i1I1ii1II1iII ) + "/local.rules" ) :
   o0o0Oo0oooo0 = open ( i1I1ii1II1iII + "/local.rules" , "w" )
   o0o0Oo0oooo0 . write ( "" )
   o0o0Oo0oooo0 . close ( )
  self . gm . push ( i1I1ii1II1iII , [ "all.rules" , "rule_state.conf" , "reports" , "*.map" , "*.config" , "local.rules" ] )
  if 42 - 42: i1 / I1iII1iiII / i1oOo0OoO + iiI1i1 / o0
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
