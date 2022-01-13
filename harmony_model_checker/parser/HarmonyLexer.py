# Generated from Harmony.g4 by ANTLR 4.9.3
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


from antlr_denter.DenterHelper import DenterHelper
from .HarmonyParser import HarmonyParser



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2u")
        buf.write("\u0354\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\t")
        buf.write("L\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT\4U\t")
        buf.write("U\4V\tV\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t[\4\\\t\\\4]\t]\4")
        buf.write("^\t^\4_\t_\4`\t`\4a\ta\4b\tb\4c\tc\4d\td\4e\te\4f\tf\4")
        buf.write("g\tg\4h\th\4i\ti\4j\tj\4k\tk\4l\tl\4m\tm\4n\tn\4o\to\4")
        buf.write("p\tp\4q\tq\4r\tr\4s\ts\4t\tt\4u\tu\4v\tv\4w\tw\4x\tx\4")
        buf.write("y\ty\4z\tz\4{\t{\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\4\3")
        buf.write("\4\3\4\3\5\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n")
        buf.write("\3\n\3\13\3\13\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3\16\3\16")
        buf.write("\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21\3\22\3\22")
        buf.write("\3\22\3\23\3\23\3\23\3\24\3\24\3\25\3\25\3\25\3\26\3\26")
        buf.write("\3\27\3\27\3\27\3\30\3\30\3\31\3\31\3\31\3\31\3\32\3\32")
        buf.write("\3\32\3\32\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\37")
        buf.write("\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3")
        buf.write(" \3 \3 \3 \3 \3 \3 \3 \3!\3!\3!\3!\3\"\3\"\3\"\3\"\3#")
        buf.write("\3#\3#\3#\3#\3$\3$\3$\3$\3$\3%\3%\3%\3%\3&\3&\3&\3&\3")
        buf.write("\'\3\'\3\'\3\'\3(\3(\3(\3(\3(\3)\3)\3)\3)\3*\3*\3*\3*")
        buf.write("\3+\3+\3+\3,\3,\3,\3-\3-\3-\3.\3.\3.\3/\3/\3/\3\60\3\60")
        buf.write("\3\60\3\61\3\61\3\61\3\62\3\62\3\62\3\62\3\63\3\63\3\63")
        buf.write("\3\64\3\64\3\64\3\64\3\64\3\65\3\65\3\65\3\65\3\66\3\66")
        buf.write("\3\66\3\66\3\67\5\67\u01c6\n\67\3\67\3\67\7\67\u01ca\n")
        buf.write("\67\f\67\16\67\u01cd\13\67\3\67\3\67\38\68\u01d2\n8\r")
        buf.write("8\168\u01d3\38\38\38\58\u01d9\n8\38\38\39\39\79\u01df")
        buf.write("\n9\f9\169\u01e2\139\39\39\39\39\79\u01e8\n9\f9\169\u01eb")
        buf.write("\139\59\u01ed\n9\3:\3:\3;\3;\3;\3<\3<\3<\3=\3=\3>\3>\3")
        buf.write("?\3?\3?\3@\3@\3A\3A\3A\3A\3A\3A\3A\3B\3B\3B\3B\3B\3B\3")
        buf.write("C\3C\3C\3C\3C\3D\3D\3D\3E\3E\3E\3E\3E\3E\3E\3E\3E\3E\3")
        buf.write("E\3E\3F\3F\3F\3G\3G\3G\3G\3G\3H\3H\3H\3H\3H\3H\3H\3I\3")
        buf.write("I\3J\3J\3J\3J\3K\3K\3L\3L\3L\3L\3L\3L\3M\3M\3M\3M\3M\3")
        buf.write("M\3N\3N\3N\3N\3N\3N\3N\3O\3O\3O\3O\3P\3P\3P\3P\3P\3Q\3")
        buf.write("Q\3Q\3Q\3Q\3Q\3Q\3Q\3Q\3R\3R\3R\3R\3R\3S\3S\3S\3S\3T\3")
        buf.write("T\3T\3T\3T\3T\3U\3U\3U\3U\3U\3U\3U\3U\3U\3U\3V\3V\3V\3")
        buf.write("W\3W\3W\3W\3W\3W\3W\3W\3W\3W\3W\3X\3X\3X\3X\3X\3Y\3Y\3")
        buf.write("Y\3Y\3Z\3Z\3Z\3[\3[\3[\3[\3[\3\\\3\\\3\\\3\\\3\\\3]\3")
        buf.write("]\3^\3^\3^\3^\3^\3^\3_\3_\3_\3_\3`\3`\3`\3`\3`\3`\3`\3")
        buf.write("a\3a\3a\3a\3a\3a\3b\3b\3c\3c\3c\3c\3d\3d\3d\3e\3e\3f\3")
        buf.write("f\3f\3f\3f\3g\3g\3g\3g\3g\3g\3g\3g\3g\3g\3g\3h\3h\3h\3")
        buf.write("h\3h\3h\3h\3h\3h\5h\u02d7\nh\3i\3i\3i\3i\3i\3i\3i\3i\3")
        buf.write("j\6j\u02e2\nj\rj\16j\u02e3\3j\3j\3j\5j\u02e9\nj\3k\3k")
        buf.write("\7k\u02ed\nk\fk\16k\u02f0\13k\3l\3l\3l\5l\u02f5\nl\3m")
        buf.write("\3m\3m\3m\6m\u02fb\nm\rm\16m\u02fc\3n\3n\3o\3o\3o\3p\3")
        buf.write("p\3p\3q\3q\3q\3r\3r\3r\3s\3s\3s\3t\3t\3t\3u\3u\3v\3v\5")
        buf.write("v\u0317\nv\3w\3w\3w\7w\u031c\nw\fw\16w\u031f\13w\3w\3")
        buf.write("w\3w\3w\7w\u0325\nw\fw\16w\u0328\13w\3w\5w\u032b\nw\3")
        buf.write("x\3x\3x\3x\3x\7x\u0332\nx\fx\16x\u0335\13x\3x\3x\3x\3")
        buf.write("x\3x\3x\3x\3x\7x\u033f\nx\fx\16x\u0342\13x\3x\3x\3x\5")
        buf.write("x\u0347\nx\3y\3y\5y\u034b\ny\3z\3z\3{\3{\3{\3{\5{\u0353")
        buf.write("\n{\5\u01e0\u0333\u0340\2|\3\3\5\4\7\5\t\6\13\7\r\b\17")
        buf.write("\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23")
        buf.write("%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67\359\36")
        buf.write(";\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63")
        buf.write("e\64g\65i\66k\67m8o9q\2s:u;w<y={>}?\177@\u0081A\u0083")
        buf.write("B\u0085C\u0087D\u0089E\u008bF\u008dG\u008fH\u0091I\u0093")
        buf.write("J\u0095K\u0097L\u0099M\u009bN\u009dO\u009fP\u00a1Q\u00a3")
        buf.write("R\u00a5S\u00a7T\u00a9U\u00abV\u00adW\u00afX\u00b1Y\u00b3")
        buf.write("Z\u00b5[\u00b7\\\u00b9]\u00bb^\u00bd_\u00bf`\u00c1a\u00c3")
        buf.write("b\u00c5c\u00c7d\u00c9e\u00cbf\u00cdg\u00cfh\u00d1i\u00d3")
        buf.write("j\u00d5k\u00d7l\u00d9m\u00db\2\u00ddn\u00dfo\u00e1p\u00e3")
        buf.write("q\u00e5r\u00e7s\u00e9t\u00ebu\u00ed\2\u00ef\2\u00f1\2")
        buf.write("\u00f3\2\u00f5\2\3\2\13\4\2\f\f\16\17\3\2\62;\5\2C\\a")
        buf.write("ac|\6\2\62;C\\aac|\3\2\60\60\5\2\62;CHch\6\2\f\f\16\17")
        buf.write("))^^\6\2\f\f\16\17$$^^\3\2^^\2\u0365\2\3\3\2\2\2\2\5\3")
        buf.write("\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2")
        buf.write("\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2")
        buf.write("\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2")
        buf.write("\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2")
        buf.write("\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3")
        buf.write("\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2")
        buf.write("\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2")
        buf.write("\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3")
        buf.write("\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W")
        buf.write("\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2")
        buf.write("a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2")
        buf.write("\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2s\3\2\2\2\2u\3\2\2")
        buf.write("\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3")
        buf.write("\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085\3\2\2\2")
        buf.write("\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2\u008b\3\2\2\2\2\u008d")
        buf.write("\3\2\2\2\2\u008f\3\2\2\2\2\u0091\3\2\2\2\2\u0093\3\2\2")
        buf.write("\2\2\u0095\3\2\2\2\2\u0097\3\2\2\2\2\u0099\3\2\2\2\2\u009b")
        buf.write("\3\2\2\2\2\u009d\3\2\2\2\2\u009f\3\2\2\2\2\u00a1\3\2\2")
        buf.write("\2\2\u00a3\3\2\2\2\2\u00a5\3\2\2\2\2\u00a7\3\2\2\2\2\u00a9")
        buf.write("\3\2\2\2\2\u00ab\3\2\2\2\2\u00ad\3\2\2\2\2\u00af\3\2\2")
        buf.write("\2\2\u00b1\3\2\2\2\2\u00b3\3\2\2\2\2\u00b5\3\2\2\2\2\u00b7")
        buf.write("\3\2\2\2\2\u00b9\3\2\2\2\2\u00bb\3\2\2\2\2\u00bd\3\2\2")
        buf.write("\2\2\u00bf\3\2\2\2\2\u00c1\3\2\2\2\2\u00c3\3\2\2\2\2\u00c5")
        buf.write("\3\2\2\2\2\u00c7\3\2\2\2\2\u00c9\3\2\2\2\2\u00cb\3\2\2")
        buf.write("\2\2\u00cd\3\2\2\2\2\u00cf\3\2\2\2\2\u00d1\3\2\2\2\2\u00d3")
        buf.write("\3\2\2\2\2\u00d5\3\2\2\2\2\u00d7\3\2\2\2\2\u00d9\3\2\2")
        buf.write("\2\2\u00dd\3\2\2\2\2\u00df\3\2\2\2\2\u00e1\3\2\2\2\2\u00e3")
        buf.write("\3\2\2\2\2\u00e5\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9\3\2\2")
        buf.write("\2\2\u00eb\3\2\2\2\3\u00f7\3\2\2\2\5\u00fb\3\2\2\2\7\u00ff")
        buf.write("\3\2\2\2\t\u0102\3\2\2\2\13\u0105\3\2\2\2\r\u0107\3\2")
        buf.write("\2\2\17\u0109\3\2\2\2\21\u010b\3\2\2\2\23\u010d\3\2\2")
        buf.write("\2\25\u010f\3\2\2\2\27\u0112\3\2\2\2\31\u0114\3\2\2\2")
        buf.write("\33\u0116\3\2\2\2\35\u011a\3\2\2\2\37\u011d\3\2\2\2!\u0120")
        buf.write("\3\2\2\2#\u0123\3\2\2\2%\u0126\3\2\2\2\'\u0129\3\2\2\2")
        buf.write(")\u012b\3\2\2\2+\u012e\3\2\2\2-\u0130\3\2\2\2/\u0133\3")
        buf.write("\2\2\2\61\u0135\3\2\2\2\63\u0139\3\2\2\2\65\u013d\3\2")
        buf.write("\2\2\67\u0141\3\2\2\29\u0149\3\2\2\2;\u0154\3\2\2\2=\u015b")
        buf.write("\3\2\2\2?\u0164\3\2\2\2A\u0170\3\2\2\2C\u0174\3\2\2\2")
        buf.write("E\u0178\3\2\2\2G\u017d\3\2\2\2I\u0182\3\2\2\2K\u0186\3")
        buf.write("\2\2\2M\u018a\3\2\2\2O\u018e\3\2\2\2Q\u0193\3\2\2\2S\u0197")
        buf.write("\3\2\2\2U\u019b\3\2\2\2W\u019e\3\2\2\2Y\u01a1\3\2\2\2")
        buf.write("[\u01a4\3\2\2\2]\u01a7\3\2\2\2_\u01aa\3\2\2\2a\u01ad\3")
        buf.write("\2\2\2c\u01b0\3\2\2\2e\u01b4\3\2\2\2g\u01b7\3\2\2\2i\u01bc")
        buf.write("\3\2\2\2k\u01c0\3\2\2\2m\u01c5\3\2\2\2o\u01d8\3\2\2\2")
        buf.write("q\u01ec\3\2\2\2s\u01ee\3\2\2\2u\u01f0\3\2\2\2w\u01f3\3")
        buf.write("\2\2\2y\u01f6\3\2\2\2{\u01f8\3\2\2\2}\u01fa\3\2\2\2\177")
        buf.write("\u01fd\3\2\2\2\u0081\u01ff\3\2\2\2\u0083\u0206\3\2\2\2")
        buf.write("\u0085\u020c\3\2\2\2\u0087\u0211\3\2\2\2\u0089\u0214\3")
        buf.write("\2\2\2\u008b\u0220\3\2\2\2\u008d\u0223\3\2\2\2\u008f\u0228")
        buf.write("\3\2\2\2\u0091\u022f\3\2\2\2\u0093\u0231\3\2\2\2\u0095")
        buf.write("\u0235\3\2\2\2\u0097\u0237\3\2\2\2\u0099\u023d\3\2\2\2")
        buf.write("\u009b\u0243\3\2\2\2\u009d\u024a\3\2\2\2\u009f\u024e\3")
        buf.write("\2\2\2\u00a1\u0253\3\2\2\2\u00a3\u025c\3\2\2\2\u00a5\u0261")
        buf.write("\3\2\2\2\u00a7\u0265\3\2\2\2\u00a9\u026b\3\2\2\2\u00ab")
        buf.write("\u0275\3\2\2\2\u00ad\u0278\3\2\2\2\u00af\u0283\3\2\2\2")
        buf.write("\u00b1\u0288\3\2\2\2\u00b3\u028c\3\2\2\2\u00b5\u028f\3")
        buf.write("\2\2\2\u00b7\u0294\3\2\2\2\u00b9\u0299\3\2\2\2\u00bb\u029b")
        buf.write("\3\2\2\2\u00bd\u02a1\3\2\2\2\u00bf\u02a5\3\2\2\2\u00c1")
        buf.write("\u02ac\3\2\2\2\u00c3\u02b2\3\2\2\2\u00c5\u02b4\3\2\2\2")
        buf.write("\u00c7\u02b8\3\2\2\2\u00c9\u02bb\3\2\2\2\u00cb\u02bd\3")
        buf.write("\2\2\2\u00cd\u02c2\3\2\2\2\u00cf\u02d6\3\2\2\2\u00d1\u02d8")
        buf.write("\3\2\2\2\u00d3\u02e8\3\2\2\2\u00d5\u02ea\3\2\2\2\u00d7")
        buf.write("\u02f1\3\2\2\2\u00d9\u02f6\3\2\2\2\u00db\u02fe\3\2\2\2")
        buf.write("\u00dd\u0300\3\2\2\2\u00df\u0303\3\2\2\2\u00e1\u0306\3")
        buf.write("\2\2\2\u00e3\u0309\3\2\2\2\u00e5\u030c\3\2\2\2\u00e7\u030f")
        buf.write("\3\2\2\2\u00e9\u0312\3\2\2\2\u00eb\u0316\3\2\2\2\u00ed")
        buf.write("\u032a\3\2\2\2\u00ef\u0346\3\2\2\2\u00f1\u034a\3\2\2\2")
        buf.write("\u00f3\u034c\3\2\2\2\u00f5\u0352\3\2\2\2\u00f7\u00f8\7")
        buf.write("\60\2\2\u00f8\u00f9\7\60\2\2\u00f9\u00fa\7\60\2\2\u00fa")
        buf.write("\4\3\2\2\2\u00fb\u00fc\7c\2\2\u00fc\u00fd\7p\2\2\u00fd")
        buf.write("\u00fe\7f\2\2\u00fe\6\3\2\2\2\u00ff\u0100\7q\2\2\u0100")
        buf.write("\u0101\7t\2\2\u0101\b\3\2\2\2\u0102\u0103\7?\2\2\u0103")
        buf.write("\u0104\7@\2\2\u0104\n\3\2\2\2\u0105\u0106\7(\2\2\u0106")
        buf.write("\f\3\2\2\2\u0107\u0108\7~\2\2\u0108\16\3\2\2\2\u0109\u010a")
        buf.write("\7`\2\2\u010a\20\3\2\2\2\u010b\u010c\7/\2\2\u010c\22\3")
        buf.write("\2\2\2\u010d\u010e\7-\2\2\u010e\24\3\2\2\2\u010f\u0110")
        buf.write("\7\61\2\2\u0110\u0111\7\61\2\2\u0111\26\3\2\2\2\u0112")
        buf.write("\u0113\7\61\2\2\u0113\30\3\2\2\2\u0114\u0115\7\'\2\2\u0115")
        buf.write("\32\3\2\2\2\u0116\u0117\7o\2\2\u0117\u0118\7q\2\2\u0118")
        buf.write("\u0119\7f\2\2\u0119\34\3\2\2\2\u011a\u011b\7,\2\2\u011b")
        buf.write("\u011c\7,\2\2\u011c\36\3\2\2\2\u011d\u011e\7>\2\2\u011e")
        buf.write("\u011f\7>\2\2\u011f \3\2\2\2\u0120\u0121\7@\2\2\u0121")
        buf.write("\u0122\7@\2\2\u0122\"\3\2\2\2\u0123\u0124\7?\2\2\u0124")
        buf.write("\u0125\7?\2\2\u0125$\3\2\2\2\u0126\u0127\7#\2\2\u0127")
        buf.write("\u0128\7?\2\2\u0128&\3\2\2\2\u0129\u012a\7>\2\2\u012a")
        buf.write("(\3\2\2\2\u012b\u012c\7>\2\2\u012c\u012d\7?\2\2\u012d")
        buf.write("*\3\2\2\2\u012e\u012f\7@\2\2\u012f,\3\2\2\2\u0130\u0131")
        buf.write("\7@\2\2\u0131\u0132\7?\2\2\u0132.\3\2\2\2\u0133\u0134")
        buf.write("\7\u0080\2\2\u0134\60\3\2\2\2\u0135\u0136\7c\2\2\u0136")
        buf.write("\u0137\7d\2\2\u0137\u0138\7u\2\2\u0138\62\3\2\2\2\u0139")
        buf.write("\u013a\7c\2\2\u013a\u013b\7n\2\2\u013b\u013c\7n\2\2\u013c")
        buf.write("\64\3\2\2\2\u013d\u013e\7c\2\2\u013e\u013f\7p\2\2\u013f")
        buf.write("\u0140\7{\2\2\u0140\66\3\2\2\2\u0141\u0142\7c\2\2\u0142")
        buf.write("\u0143\7v\2\2\u0143\u0144\7N\2\2\u0144\u0145\7c\2\2\u0145")
        buf.write("\u0146\7d\2\2\u0146\u0147\7g\2\2\u0147\u0148\7n\2\2\u0148")
        buf.write("8\3\2\2\2\u0149\u014a\7e\2\2\u014a\u014b\7q\2\2\u014b")
        buf.write("\u014c\7w\2\2\u014c\u014d\7p\2\2\u014d\u014e\7v\2\2\u014e")
        buf.write("\u014f\7N\2\2\u014f\u0150\7c\2\2\u0150\u0151\7d\2\2\u0151")
        buf.write("\u0152\7g\2\2\u0152\u0153\7n\2\2\u0153:\3\2\2\2\u0154")
        buf.write("\u0155\7e\2\2\u0155\u0156\7j\2\2\u0156\u0157\7q\2\2\u0157")
        buf.write("\u0158\7q\2\2\u0158\u0159\7u\2\2\u0159\u015a\7g\2\2\u015a")
        buf.write("<\3\2\2\2\u015b\u015c\7e\2\2\u015c\u015d\7q\2\2\u015d")
        buf.write("\u015e\7p\2\2\u015e\u015f\7v\2\2\u015f\u0160\7g\2\2\u0160")
        buf.write("\u0161\7z\2\2\u0161\u0162\7v\2\2\u0162\u0163\7u\2\2\u0163")
        buf.write(">\3\2\2\2\u0164\u0165\7i\2\2\u0165\u0166\7g\2\2\u0166")
        buf.write("\u0167\7v\2\2\u0167\u0168\7a\2\2\u0168\u0169\7e\2\2\u0169")
        buf.write("\u016a\7q\2\2\u016a\u016b\7p\2\2\u016b\u016c\7v\2\2\u016c")
        buf.write("\u016d\7g\2\2\u016d\u016e\7z\2\2\u016e\u016f\7v\2\2\u016f")
        buf.write("@\3\2\2\2\u0170\u0171\7o\2\2\u0171\u0172\7k\2\2\u0172")
        buf.write("\u0173\7p\2\2\u0173B\3\2\2\2\u0174\u0175\7o\2\2\u0175")
        buf.write("\u0176\7c\2\2\u0176\u0177\7z\2\2\u0177D\3\2\2\2\u0178")
        buf.write("\u0179\7m\2\2\u0179\u017a\7g\2\2\u017a\u017b\7{\2\2\u017b")
        buf.write("\u017c\7u\2\2\u017cF\3\2\2\2\u017d\u017e\7j\2\2\u017e")
        buf.write("\u017f\7c\2\2\u017f\u0180\7u\2\2\u0180\u0181\7j\2\2\u0181")
        buf.write("H\3\2\2\2\u0182\u0183\7n\2\2\u0183\u0184\7g\2\2\u0184")
        buf.write("\u0185\7p\2\2\u0185J\3\2\2\2\u0186\u0187\7u\2\2\u0187")
        buf.write("\u0188\7v\2\2\u0188\u0189\7t\2\2\u0189L\3\2\2\2\u018a")
        buf.write("\u018b\7g\2\2\u018b\u018c\7p\2\2\u018c\u018d\7f\2\2\u018d")
        buf.write("N\3\2\2\2\u018e\u018f\7c\2\2\u018f\u0190\7p\2\2\u0190")
        buf.write("\u0191\7f\2\2\u0191\u0192\7?\2\2\u0192P\3\2\2\2\u0193")
        buf.write("\u0194\7q\2\2\u0194\u0195\7t\2\2\u0195\u0196\7?\2\2\u0196")
        buf.write("R\3\2\2\2\u0197\u0198\7?\2\2\u0198\u0199\7@\2\2\u0199")
        buf.write("\u019a\7?\2\2\u019aT\3\2\2\2\u019b\u019c\7(\2\2\u019c")
        buf.write("\u019d\7?\2\2\u019dV\3\2\2\2\u019e\u019f\7~\2\2\u019f")
        buf.write("\u01a0\7?\2\2\u01a0X\3\2\2\2\u01a1\u01a2\7`\2\2\u01a2")
        buf.write("\u01a3\7?\2\2\u01a3Z\3\2\2\2\u01a4\u01a5\7/\2\2\u01a5")
        buf.write("\u01a6\7?\2\2\u01a6\\\3\2\2\2\u01a7\u01a8\7-\2\2\u01a8")
        buf.write("\u01a9\7?\2\2\u01a9^\3\2\2\2\u01aa\u01ab\7,\2\2\u01ab")
        buf.write("\u01ac\7?\2\2\u01ac`\3\2\2\2\u01ad\u01ae\7\61\2\2\u01ae")
        buf.write("\u01af\7?\2\2\u01afb\3\2\2\2\u01b0\u01b1\7\61\2\2\u01b1")
        buf.write("\u01b2\7\61\2\2\u01b2\u01b3\7?\2\2\u01b3d\3\2\2\2\u01b4")
        buf.write("\u01b5\7\'\2\2\u01b5\u01b6\7?\2\2\u01b6f\3\2\2\2\u01b7")
        buf.write("\u01b8\7o\2\2\u01b8\u01b9\7q\2\2\u01b9\u01ba\7f\2\2\u01ba")
        buf.write("\u01bb\7?\2\2\u01bbh\3\2\2\2\u01bc\u01bd\7,\2\2\u01bd")
        buf.write("\u01be\7,\2\2\u01be\u01bf\7?\2\2\u01bfj\3\2\2\2\u01c0")
        buf.write("\u01c1\7@\2\2\u01c1\u01c2\7@\2\2\u01c2\u01c3\7?\2\2\u01c3")
        buf.write("l\3\2\2\2\u01c4\u01c6\7\17\2\2\u01c5\u01c4\3\2\2\2\u01c5")
        buf.write("\u01c6\3\2\2\2\u01c6\u01c7\3\2\2\2\u01c7\u01cb\7\f\2\2")
        buf.write("\u01c8\u01ca\7\"\2\2\u01c9\u01c8\3\2\2\2\u01ca\u01cd\3")
        buf.write("\2\2\2\u01cb\u01c9\3\2\2\2\u01cb\u01cc\3\2\2\2\u01cc\u01ce")
        buf.write("\3\2\2\2\u01cd\u01cb\3\2\2\2\u01ce\u01cf\b\67\2\2\u01cf")
        buf.write("n\3\2\2\2\u01d0\u01d2\7\"\2\2\u01d1\u01d0\3\2\2\2\u01d2")
        buf.write("\u01d3\3\2\2\2\u01d3\u01d1\3\2\2\2\u01d3\u01d4\3\2\2\2")
        buf.write("\u01d4\u01d9\3\2\2\2\u01d5\u01d6\7^\2\2\u01d6\u01d9\5")
        buf.write("m\67\2\u01d7\u01d9\5q9\2\u01d8\u01d1\3\2\2\2\u01d8\u01d5")
        buf.write("\3\2\2\2\u01d8\u01d7\3\2\2\2\u01d9\u01da\3\2\2\2\u01da")
        buf.write("\u01db\b8\3\2\u01dbp\3\2\2\2\u01dc\u01e0\5u;\2\u01dd\u01df")
        buf.write("\13\2\2\2\u01de\u01dd\3\2\2\2\u01df\u01e2\3\2\2\2\u01e0")
        buf.write("\u01e1\3\2\2\2\u01e0\u01de\3\2\2\2\u01e1\u01e3\3\2\2\2")
        buf.write("\u01e2\u01e0\3\2\2\2\u01e3\u01e4\5w<\2\u01e4\u01ed\3\2")
        buf.write("\2\2\u01e5\u01e9\5s:\2\u01e6\u01e8\n\2\2\2\u01e7\u01e6")
        buf.write("\3\2\2\2\u01e8\u01eb\3\2\2\2\u01e9\u01e7\3\2\2\2\u01e9")
        buf.write("\u01ea\3\2\2\2\u01ea\u01ed\3\2\2\2\u01eb\u01e9\3\2\2\2")
        buf.write("\u01ec\u01dc\3\2\2\2\u01ec\u01e5\3\2\2\2\u01edr\3\2\2")
        buf.write("\2\u01ee\u01ef\7%\2\2\u01eft\3\2\2\2\u01f0\u01f1\7*\2")
        buf.write("\2\u01f1\u01f2\7,\2\2\u01f2v\3\2\2\2\u01f3\u01f4\7,\2")
        buf.write("\2\u01f4\u01f5\7+\2\2\u01f5x\3\2\2\2\u01f6\u01f7\7#\2")
        buf.write("\2\u01f7z\3\2\2\2\u01f8\u01f9\7,\2\2\u01f9|\3\2\2\2\u01fa")
        buf.write("\u01fb\7c\2\2\u01fb\u01fc\7u\2\2\u01fc~\3\2\2\2\u01fd")
        buf.write("\u01fe\7\60\2\2\u01fe\u0080\3\2\2\2\u01ff\u0200\7k\2\2")
        buf.write("\u0200\u0201\7o\2\2\u0201\u0202\7r\2\2\u0202\u0203\7q")
        buf.write("\2\2\u0203\u0204\7t\2\2\u0204\u0205\7v\2\2\u0205\u0082")
        buf.write("\3\2\2\2\u0206\u0207\7r\2\2\u0207\u0208\7t\2\2\u0208\u0209")
        buf.write("\7k\2\2\u0209\u020a\7p\2\2\u020a\u020b\7v\2\2\u020b\u0084")
        buf.write("\3\2\2\2\u020c\u020d\7h\2\2\u020d\u020e\7t\2\2\u020e\u020f")
        buf.write("\7q\2\2\u020f\u0210\7o\2\2\u0210\u0086\3\2\2\2\u0211\u0212")
        buf.write("\7\60\2\2\u0212\u0213\7\60\2\2\u0213\u0088\3\2\2\2\u0214")
        buf.write("\u0215\7u\2\2\u0215\u0216\7g\2\2\u0216\u0217\7v\2\2\u0217")
        buf.write("\u0218\7k\2\2\u0218\u0219\7p\2\2\u0219\u021a\7v\2\2\u021a")
        buf.write("\u021b\7n\2\2\u021b\u021c\7g\2\2\u021c\u021d\7x\2\2\u021d")
        buf.write("\u021e\7g\2\2\u021e\u021f\7n\2\2\u021f\u008a\3\2\2\2\u0220")
        buf.write("\u0221\7/\2\2\u0221\u0222\7@\2\2\u0222\u008c\3\2\2\2\u0223")
        buf.write("\u0224\7u\2\2\u0224\u0225\7v\2\2\u0225\u0226\7q\2\2\u0226")
        buf.write("\u0227\7r\2\2\u0227\u008e\3\2\2\2\u0228\u0229\7n\2\2\u0229")
        buf.write("\u022a\7c\2\2\u022a\u022b\7o\2\2\u022b\u022c\7d\2\2\u022c")
        buf.write("\u022d\7f\2\2\u022d\u022e\7c\2\2\u022e\u0090\3\2\2\2\u022f")
        buf.write("\u0230\7A\2\2\u0230\u0092\3\2\2\2\u0231\u0232\7p\2\2\u0232")
        buf.write("\u0233\7q\2\2\u0233\u0234\7v\2\2\u0234\u0094\3\2\2\2\u0235")
        buf.write("\u0236\7.\2\2\u0236\u0096\3\2\2\2\u0237\u0238\7e\2\2\u0238")
        buf.write("\u0239\7q\2\2\u0239\u023a\7p\2\2\u023a\u023b\7u\2\2\u023b")
        buf.write("\u023c\7v\2\2\u023c\u0098\3\2\2\2\u023d\u023e\7c\2\2\u023e")
        buf.write("\u023f\7y\2\2\u023f\u0240\7c\2\2\u0240\u0241\7k\2\2\u0241")
        buf.write("\u0242\7v\2\2\u0242\u009a\3\2\2\2\u0243\u0244\7c\2\2\u0244")
        buf.write("\u0245\7u\2\2\u0245\u0246\7u\2\2\u0246\u0247\7g\2\2\u0247")
        buf.write("\u0248\7t\2\2\u0248\u0249\7v\2\2\u0249\u009c\3\2\2\2\u024a")
        buf.write("\u024b\7x\2\2\u024b\u024c\7c\2\2\u024c\u024d\7t\2\2\u024d")
        buf.write("\u009e\3\2\2\2\u024e\u024f\7v\2\2\u024f\u0250\7t\2\2\u0250")
        buf.write("\u0251\7c\2\2\u0251\u0252\7r\2\2\u0252\u00a0\3\2\2\2\u0253")
        buf.write("\u0254\7r\2\2\u0254\u0255\7q\2\2\u0255\u0256\7u\2\2\u0256")
        buf.write("\u0257\7u\2\2\u0257\u0258\7k\2\2\u0258\u0259\7d\2\2\u0259")
        buf.write("\u025a\7n\2\2\u025a\u025b\7{\2\2\u025b\u00a2\3\2\2\2\u025c")
        buf.write("\u025d\7r\2\2\u025d\u025e\7c\2\2\u025e\u025f\7u\2\2\u025f")
        buf.write("\u0260\7u\2\2\u0260\u00a4\3\2\2\2\u0261\u0262\7f\2\2\u0262")
        buf.write("\u0263\7g\2\2\u0263\u0264\7n\2\2\u0264\u00a6\3\2\2\2\u0265")
        buf.write("\u0266\7u\2\2\u0266\u0267\7r\2\2\u0267\u0268\7c\2\2\u0268")
        buf.write("\u0269\7y\2\2\u0269\u026a\7p\2\2\u026a\u00a8\3\2\2\2\u026b")
        buf.write("\u026c\7k\2\2\u026c\u026d\7p\2\2\u026d\u026e\7x\2\2\u026e")
        buf.write("\u026f\7c\2\2\u026f\u0270\7t\2\2\u0270\u0271\7k\2\2\u0271")
        buf.write("\u0272\7c\2\2\u0272\u0273\7p\2\2\u0273\u0274\7v\2\2\u0274")
        buf.write("\u00aa\3\2\2\2\u0275\u0276\7i\2\2\u0276\u0277\7q\2\2\u0277")
        buf.write("\u00ac\3\2\2\2\u0278\u0279\7u\2\2\u0279\u027a\7g\2\2\u027a")
        buf.write("\u027b\7s\2\2\u027b\u027c\7w\2\2\u027c\u027d\7g\2\2\u027d")
        buf.write("\u027e\7p\2\2\u027e\u027f\7v\2\2\u027f\u0280\7k\2\2\u0280")
        buf.write("\u0281\7c\2\2\u0281\u0282\7n\2\2\u0282\u00ae\3\2\2\2\u0283")
        buf.write("\u0284\7y\2\2\u0284\u0285\7j\2\2\u0285\u0286\7g\2\2\u0286")
        buf.write("\u0287\7p\2\2\u0287\u00b0\3\2\2\2\u0288\u0289\7n\2\2\u0289")
        buf.write("\u028a\7g\2\2\u028a\u028b\7v\2\2\u028b\u00b2\3\2\2\2\u028c")
        buf.write("\u028d\7k\2\2\u028d\u028e\7h\2\2\u028e\u00b4\3\2\2\2\u028f")
        buf.write("\u0290\7g\2\2\u0290\u0291\7n\2\2\u0291\u0292\7k\2\2\u0292")
        buf.write("\u0293\7h\2\2\u0293\u00b6\3\2\2\2\u0294\u0295\7g\2\2\u0295")
        buf.write("\u0296\7n\2\2\u0296\u0297\7u\2\2\u0297\u0298\7g\2\2\u0298")
        buf.write("\u00b8\3\2\2\2\u0299\u029a\7B\2\2\u029a\u00ba\3\2\2\2")
        buf.write("\u029b\u029c\7y\2\2\u029c\u029d\7j\2\2\u029d\u029e\7k")
        buf.write("\2\2\u029e\u029f\7n\2\2\u029f\u02a0\7g\2\2\u02a0\u00bc")
        buf.write("\3\2\2\2\u02a1\u02a2\7f\2\2\u02a2\u02a3\7g\2\2\u02a3\u02a4")
        buf.write("\7h\2\2\u02a4\u00be\3\2\2\2\u02a5\u02a6\7g\2\2\u02a6\u02a7")
        buf.write("\7z\2\2\u02a7\u02a8\7k\2\2\u02a8\u02a9\7u\2\2\u02a9\u02aa")
        buf.write("\7v\2\2\u02aa\u02ab\7u\2\2\u02ab\u00c0\3\2\2\2\u02ac\u02ad")
        buf.write("\7y\2\2\u02ad\u02ae\7j\2\2\u02ae\u02af\7g\2\2\u02af\u02b0")
        buf.write("\7t\2\2\u02b0\u02b1\7g\2\2\u02b1\u00c2\3\2\2\2\u02b2\u02b3")
        buf.write("\7?\2\2\u02b3\u00c4\3\2\2\2\u02b4\u02b5\7h\2\2\u02b5\u02b6")
        buf.write("\7q\2\2\u02b6\u02b7\7t\2\2\u02b7\u00c6\3\2\2\2\u02b8\u02b9")
        buf.write("\7k\2\2\u02b9\u02ba\7p\2\2\u02ba\u00c8\3\2\2\2\u02bb\u02bc")
        buf.write("\7<\2\2\u02bc\u00ca\3\2\2\2\u02bd\u02be\7P\2\2\u02be\u02bf")
        buf.write("\7q\2\2\u02bf\u02c0\7p\2\2\u02c0\u02c1\7g\2\2\u02c1\u00cc")
        buf.write("\3\2\2\2\u02c2\u02c3\7c\2\2\u02c3\u02c4\7v\2\2\u02c4\u02c5")
        buf.write("\7q\2\2\u02c5\u02c6\7o\2\2\u02c6\u02c7\7k\2\2\u02c7\u02c8")
        buf.write("\7e\2\2\u02c8\u02c9\7c\2\2\u02c9\u02ca\7n\2\2\u02ca\u02cb")
        buf.write("\7n\2\2\u02cb\u02cc\7{\2\2\u02cc\u00ce\3\2\2\2\u02cd\u02ce")
        buf.write("\7H\2\2\u02ce\u02cf\7c\2\2\u02cf\u02d0\7n\2\2\u02d0\u02d1")
        buf.write("\7u\2\2\u02d1\u02d7\7g\2\2\u02d2\u02d3\7V\2\2\u02d3\u02d4")
        buf.write("\7t\2\2\u02d4\u02d5\7w\2\2\u02d5\u02d7\7g\2\2\u02d6\u02cd")
        buf.write("\3\2\2\2\u02d6\u02d2\3\2\2\2\u02d7\u00d0\3\2\2\2\u02d8")
        buf.write("\u02d9\7g\2\2\u02d9\u02da\7v\2\2\u02da\u02db\7g\2\2\u02db")
        buf.write("\u02dc\7t\2\2\u02dc\u02dd\7p\2\2\u02dd\u02de\7c\2\2\u02de")
        buf.write("\u02df\7n\2\2\u02df\u00d2\3\2\2\2\u02e0\u02e2\t\3\2\2")
        buf.write("\u02e1\u02e0\3\2\2\2\u02e2\u02e3\3\2\2\2\u02e3\u02e1\3")
        buf.write("\2\2\2\u02e3\u02e4\3\2\2\2\u02e4\u02e9\3\2\2\2\u02e5\u02e6")
        buf.write("\7k\2\2\u02e6\u02e7\7p\2\2\u02e7\u02e9\7h\2\2\u02e8\u02e1")
        buf.write("\3\2\2\2\u02e8\u02e5\3\2\2\2\u02e9\u00d4\3\2\2\2\u02ea")
        buf.write("\u02ee\t\4\2\2\u02eb\u02ed\t\5\2\2\u02ec\u02eb\3\2\2\2")
        buf.write("\u02ed\u02f0\3\2\2\2\u02ee\u02ec\3\2\2\2\u02ee\u02ef\3")
        buf.write("\2\2\2\u02ef\u00d6\3\2\2\2\u02f0\u02ee\3\2\2\2\u02f1\u02f4")
        buf.write("\t\6\2\2\u02f2\u02f5\5\u00d9m\2\u02f3\u02f5\5\u00d5k\2")
        buf.write("\u02f4\u02f2\3\2\2\2\u02f4\u02f3\3\2\2\2\u02f5\u00d8\3")
        buf.write("\2\2\2\u02f6\u02f7\7\62\2\2\u02f7\u02f8\7Z\2\2\u02f8\u02fa")
        buf.write("\3\2\2\2\u02f9\u02fb\5\u00dbn\2\u02fa\u02f9\3\2\2\2\u02fb")
        buf.write("\u02fc\3\2\2\2\u02fc\u02fa\3\2\2\2\u02fc\u02fd\3\2\2\2")
        buf.write("\u02fd\u00da\3\2\2\2\u02fe\u02ff\t\7\2\2\u02ff\u00dc\3")
        buf.write("\2\2\2\u0300\u0301\7]\2\2\u0301\u0302\bo\4\2\u0302\u00de")
        buf.write("\3\2\2\2\u0303\u0304\7_\2\2\u0304\u0305\bp\5\2\u0305\u00e0")
        buf.write("\3\2\2\2\u0306\u0307\7}\2\2\u0307\u0308\bq\6\2\u0308\u00e2")
        buf.write("\3\2\2\2\u0309\u030a\7\177\2\2\u030a\u030b\br\7\2\u030b")
        buf.write("\u00e4\3\2\2\2\u030c\u030d\7*\2\2\u030d\u030e\bs\b\2\u030e")
        buf.write("\u00e6\3\2\2\2\u030f\u0310\7+\2\2\u0310\u0311\bt\t\2\u0311")
        buf.write("\u00e8\3\2\2\2\u0312\u0313\7=\2\2\u0313\u00ea\3\2\2\2")
        buf.write("\u0314\u0317\5\u00edw\2\u0315\u0317\5\u00efx\2\u0316\u0314")
        buf.write("\3\2\2\2\u0316\u0315\3\2\2\2\u0317\u00ec\3\2\2\2\u0318")
        buf.write("\u031d\7)\2\2\u0319\u031c\5\u00f5{\2\u031a\u031c\n\b\2")
        buf.write("\2\u031b\u0319\3\2\2\2\u031b\u031a\3\2\2\2\u031c\u031f")
        buf.write("\3\2\2\2\u031d\u031b\3\2\2\2\u031d\u031e\3\2\2\2\u031e")
        buf.write("\u0320\3\2\2\2\u031f\u031d\3\2\2\2\u0320\u032b\7)\2\2")
        buf.write("\u0321\u0326\7$\2\2\u0322\u0325\5\u00f5{\2\u0323\u0325")
        buf.write("\n\t\2\2\u0324\u0322\3\2\2\2\u0324\u0323\3\2\2\2\u0325")
        buf.write("\u0328\3\2\2\2\u0326\u0324\3\2\2\2\u0326\u0327\3\2\2\2")
        buf.write("\u0327\u0329\3\2\2\2\u0328\u0326\3\2\2\2\u0329\u032b\7")
        buf.write("$\2\2\u032a\u0318\3\2\2\2\u032a\u0321\3\2\2\2\u032b\u00ee")
        buf.write("\3\2\2\2\u032c\u032d\7)\2\2\u032d\u032e\7)\2\2\u032e\u032f")
        buf.write("\7)\2\2\u032f\u0333\3\2\2\2\u0330\u0332\5\u00f1y\2\u0331")
        buf.write("\u0330\3\2\2\2\u0332\u0335\3\2\2\2\u0333\u0334\3\2\2\2")
        buf.write("\u0333\u0331\3\2\2\2\u0334\u0336\3\2\2\2\u0335\u0333\3")
        buf.write("\2\2\2\u0336\u0337\7)\2\2\u0337\u0338\7)\2\2\u0338\u0347")
        buf.write("\7)\2\2\u0339\u033a\7$\2\2\u033a\u033b\7$\2\2\u033b\u033c")
        buf.write("\7$\2\2\u033c\u0340\3\2\2\2\u033d\u033f\5\u00f1y\2\u033e")
        buf.write("\u033d\3\2\2\2\u033f\u0342\3\2\2\2\u0340\u0341\3\2\2\2")
        buf.write("\u0340\u033e\3\2\2\2\u0341\u0343\3\2\2\2\u0342\u0340\3")
        buf.write("\2\2\2\u0343\u0344\7$\2\2\u0344\u0345\7$\2\2\u0345\u0347")
        buf.write("\7$\2\2\u0346\u032c\3\2\2\2\u0346\u0339\3\2\2\2\u0347")
        buf.write("\u00f0\3\2\2\2\u0348\u034b\5\u00f3z\2\u0349\u034b\5\u00f5")
        buf.write("{\2\u034a\u0348\3\2\2\2\u034a\u0349\3\2\2\2\u034b\u00f2")
        buf.write("\3\2\2\2\u034c\u034d\n\n\2\2\u034d\u00f4\3\2\2\2\u034e")
        buf.write("\u034f\7^\2\2\u034f\u0353\13\2\2\2\u0350\u0351\7^\2\2")
        buf.write("\u0351\u0353\5m\67\2\u0352\u034e\3\2\2\2\u0352\u0350\3")
        buf.write("\2\2\2\u0353\u00f6\3\2\2\2\33\2\u01c5\u01cb\u01d3\u01d8")
        buf.write("\u01e0\u01e9\u01ec\u02d6\u02e3\u02e8\u02ee\u02f4\u02fc")
        buf.write("\u0316\u031b\u031d\u0324\u0326\u032a\u0333\u0340\u0346")
        buf.write("\u034a\u0352\n\3\67\2\b\2\2\3o\3\3p\4\3q\5\3r\6\3s\7\3")
        buf.write("t\b")
        return buf.getvalue()


class HarmonyLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    T__17 = 18
    T__18 = 19
    T__19 = 20
    T__20 = 21
    T__21 = 22
    T__22 = 23
    T__23 = 24
    T__24 = 25
    T__25 = 26
    T__26 = 27
    T__27 = 28
    T__28 = 29
    T__29 = 30
    T__30 = 31
    T__31 = 32
    T__32 = 33
    T__33 = 34
    T__34 = 35
    T__35 = 36
    T__36 = 37
    T__37 = 38
    T__38 = 39
    T__39 = 40
    T__40 = 41
    T__41 = 42
    T__42 = 43
    T__43 = 44
    T__44 = 45
    T__45 = 46
    T__46 = 47
    T__47 = 48
    T__48 = 49
    T__49 = 50
    T__50 = 51
    T__51 = 52
    T__52 = 53
    NL = 54
    WS = 55
    COMMENT_START = 56
    OPEN_MULTI_COMMENT = 57
    CLOSE_MULTI_COMMENT = 58
    POINTER_OF = 59
    STAR = 60
    AS = 61
    DOT = 62
    IMPORT = 63
    PRINT = 64
    FROM = 65
    RANGE = 66
    SETINTLEVEL = 67
    ARROW = 68
    STOP = 69
    LAMBDA = 70
    ADDRESS_OF = 71
    NOT = 72
    COMMA = 73
    CONST = 74
    AWAIT = 75
    ASSERT = 76
    VAR = 77
    TRAP = 78
    POSSIBLY = 79
    PASS = 80
    DEL = 81
    SPAWN = 82
    INVARIANT = 83
    GO = 84
    SEQUENTIAL = 85
    WHEN = 86
    LET = 87
    IF = 88
    ELIF = 89
    ELSE = 90
    AT = 91
    WHILE = 92
    DEF = 93
    EXISTS = 94
    WHERE = 95
    EQ = 96
    FOR = 97
    IN = 98
    COLON = 99
    NONE = 100
    ATOMICALLY = 101
    BOOL = 102
    ETERNAL = 103
    INT = 104
    NAME = 105
    ATOM = 106
    HEX_INTEGER = 107
    OPEN_BRACK = 108
    CLOSE_BRACK = 109
    OPEN_BRACES = 110
    CLOSE_BRACES = 111
    OPEN_PAREN = 112
    CLOSE_PAREN = 113
    SEMI_COLON = 114
    STRING = 115

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'...'", "'and'", "'or'", "'=>'", "'&'", "'|'", "'^'", "'-'", 
            "'+'", "'//'", "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", 
            "'=='", "'!='", "'<'", "'<='", "'>'", "'>='", "'~'", "'abs'", 
            "'all'", "'any'", "'atLabel'", "'countLabel'", "'choose'", "'contexts'", 
            "'get_context'", "'min'", "'max'", "'keys'", "'hash'", "'len'", 
            "'str'", "'end'", "'and='", "'or='", "'=>='", "'&='", "'|='", 
            "'^='", "'-='", "'+='", "'*='", "'/='", "'//='", "'%='", "'mod='", 
            "'**='", "'>>='", "'#'", "'(*'", "'*)'", "'!'", "'*'", "'as'", 
            "'.'", "'import'", "'print'", "'from'", "'..'", "'setintlevel'", 
            "'->'", "'stop'", "'lambda'", "'?'", "'not'", "','", "'const'", 
            "'await'", "'assert'", "'var'", "'trap'", "'possibly'", "'pass'", 
            "'del'", "'spawn'", "'invariant'", "'go'", "'sequential'", "'when'", 
            "'let'", "'if'", "'elif'", "'else'", "'@'", "'while'", "'def'", 
            "'exists'", "'where'", "'='", "'for'", "'in'", "':'", "'None'", 
            "'atomically'", "'eternal'", "'['", "']'", "'{'", "'}'", "'('", 
            "')'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "NL", "WS", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
            "POINTER_OF", "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", 
            "RANGE", "SETINTLEVEL", "ARROW", "STOP", "LAMBDA", "ADDRESS_OF", 
            "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", "VAR", "TRAP", "POSSIBLY", 
            "PASS", "DEL", "SPAWN", "INVARIANT", "GO", "SEQUENTIAL", "WHEN", 
            "LET", "IF", "ELIF", "ELSE", "AT", "WHILE", "DEF", "EXISTS", 
            "WHERE", "EQ", "FOR", "IN", "COLON", "NONE", "ATOMICALLY", "BOOL", 
            "ETERNAL", "INT", "NAME", "ATOM", "HEX_INTEGER", "OPEN_BRACK", 
            "CLOSE_BRACK", "OPEN_BRACES", "CLOSE_BRACES", "OPEN_PAREN", 
            "CLOSE_PAREN", "SEMI_COLON", "STRING" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "T__20", "T__21", "T__22", "T__23", "T__24", "T__25", 
                  "T__26", "T__27", "T__28", "T__29", "T__30", "T__31", 
                  "T__32", "T__33", "T__34", "T__35", "T__36", "T__37", 
                  "T__38", "T__39", "T__40", "T__41", "T__42", "T__43", 
                  "T__44", "T__45", "T__46", "T__47", "T__48", "T__49", 
                  "T__50", "T__51", "T__52", "NL", "WS", "COMMENT", "COMMENT_START", 
                  "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", "POINTER_OF", 
                  "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", "RANGE", 
                  "SETINTLEVEL", "ARROW", "STOP", "LAMBDA", "ADDRESS_OF", 
                  "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", "VAR", "TRAP", 
                  "POSSIBLY", "PASS", "DEL", "SPAWN", "INVARIANT", "GO", 
                  "SEQUENTIAL", "WHEN", "LET", "IF", "ELIF", "ELSE", "AT", 
                  "WHILE", "DEF", "EXISTS", "WHERE", "EQ", "FOR", "IN", 
                  "COLON", "NONE", "ATOMICALLY", "BOOL", "ETERNAL", "INT", 
                  "NAME", "ATOM", "HEX_INTEGER", "HEX_DIGIT", "OPEN_BRACK", 
                  "CLOSE_BRACK", "OPEN_BRACES", "CLOSE_BRACES", "OPEN_PAREN", 
                  "CLOSE_PAREN", "SEMI_COLON", "STRING", "SHORT_STRING", 
                  "LONG_STRING", "LONG_STRING_ITEM", "LONG_STRING_CHAR", 
                  "STRING_ESCAPE_SEQ" ]

    grammarFileName = "Harmony.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    class MyCoolDenter(DenterHelper):
        def __init__(self, lexer, nl_token, indent_token, dedent_token, ignore_eof):
            super().__init__(nl_token, indent_token, dedent_token, ignore_eof)
            self.lexer: HarmonyLexer = lexer

        def pull_token(self):
            return super(HarmonyLexer, self.lexer).nextToken()

    @property
    def opened(self):
        try:
            return self._opened
        except AttributeError:
            self._opened = 0
            return self._opened

    @opened.setter
    def opened(self, value):
        self._opened = value

    denter = None

    def nextToken(self):
        if not self.denter:
            self.denter = self.MyCoolDenter(self, self.NL, HarmonyParser.INDENT, HarmonyParser.DEDENT, ignore_eof=False)
        token = self.denter.next_token()
        return token


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[53] = self.NL_action 
            actions[109] = self.OPEN_BRACK_action 
            actions[110] = self.CLOSE_BRACK_action 
            actions[111] = self.OPEN_BRACES_action 
            actions[112] = self.CLOSE_BRACES_action 
            actions[113] = self.OPEN_PAREN_action 
            actions[114] = self.CLOSE_PAREN_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def NL_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:

            if self.opened:
                self.skip()

     

    def OPEN_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            self.opened += 1
     

    def CLOSE_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:
            self.opened -= 1
     

    def OPEN_BRACES_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:
            self.opened += 1
     

    def CLOSE_BRACES_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:
            self.opened -= 1
     

    def OPEN_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 5:
            self.opened += 1
     

    def CLOSE_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 6:
            self.opened -= 1
     


