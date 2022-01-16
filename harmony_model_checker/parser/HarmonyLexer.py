# Generated from Harmony.g4 by ANTLR 4.9.3
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


from .custom_denter import ModifiedDenterHelper
from .HarmonyParser import HarmonyParser



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2u")
        buf.write("\u035b\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("\67\f\67\16\67\u01cd\13\67\3\67\5\67\u01d0\n\67\3\67\3")
        buf.write("\67\38\68\u01d5\n8\r8\168\u01d6\38\38\38\58\u01dc\n8\3")
        buf.write("8\38\39\39\79\u01e2\n9\f9\169\u01e5\139\39\39\39\39\7")
        buf.write("9\u01eb\n9\f9\169\u01ee\139\59\u01f0\n9\3:\3:\3;\3;\3")
        buf.write(";\3<\3<\3<\3=\3=\3>\3>\3?\3?\3?\3@\3@\3A\3A\3A\3A\3A\3")
        buf.write("A\3A\3B\3B\3B\3B\3B\3B\3C\3C\3C\3C\3C\3D\3D\3D\3E\3E\3")
        buf.write("E\3E\3E\3E\3E\3E\3E\3E\3E\3E\3F\3F\3F\3G\3G\3G\3G\3G\3")
        buf.write("H\3H\3H\3H\3H\3H\3H\3I\3I\3J\3J\3J\3J\3K\3K\3L\3L\3L\3")
        buf.write("L\3L\3L\3M\3M\3M\3M\3M\3M\3N\3N\3N\3N\3N\3N\3N\3O\3O\3")
        buf.write("O\3O\3P\3P\3P\3P\3P\3Q\3Q\3Q\3Q\3Q\3Q\3Q\3Q\3Q\3R\3R\3")
        buf.write("R\3R\3R\3S\3S\3S\3S\3T\3T\3T\3T\3T\3T\3U\3U\3U\3U\3U\3")
        buf.write("U\3U\3U\3U\3U\3V\3V\3V\3W\3W\3W\3W\3W\3W\3W\3W\3W\3W\3")
        buf.write("W\3X\3X\3X\3X\3X\3Y\3Y\3Y\3Y\3Z\3Z\3Z\3[\3[\3[\3[\3[\3")
        buf.write("\\\3\\\3\\\3\\\3\\\3]\3]\3^\3^\3^\3^\3^\3^\3_\3_\3_\3")
        buf.write("_\3`\3`\3`\3`\3`\3`\3`\3a\3a\3a\3a\3a\3a\3b\3b\3c\3c\3")
        buf.write("c\3c\3c\3c\3d\3d\3d\3d\3d\3e\3e\3f\3f\3f\3f\3f\3g\3g\3")
        buf.write("g\3g\3g\3g\3g\3g\3g\3g\3g\3h\3h\3h\3h\3h\3h\3h\3h\3h\5")
        buf.write("h\u02de\nh\3i\3i\3i\3i\3i\3i\3i\3i\3j\6j\u02e9\nj\rj\16")
        buf.write("j\u02ea\3j\3j\3j\5j\u02f0\nj\3k\3k\7k\u02f4\nk\fk\16k")
        buf.write("\u02f7\13k\3l\3l\3l\5l\u02fc\nl\3m\3m\3m\3m\6m\u0302\n")
        buf.write("m\rm\16m\u0303\3n\3n\3o\3o\3o\3p\3p\3p\3q\3q\3q\3r\3r")
        buf.write("\3r\3s\3s\3s\3t\3t\3t\3u\3u\3v\3v\5v\u031e\nv\3w\3w\3")
        buf.write("w\7w\u0323\nw\fw\16w\u0326\13w\3w\3w\3w\3w\7w\u032c\n")
        buf.write("w\fw\16w\u032f\13w\3w\5w\u0332\nw\3x\3x\3x\3x\3x\7x\u0339")
        buf.write("\nx\fx\16x\u033c\13x\3x\3x\3x\3x\3x\3x\3x\3x\7x\u0346")
        buf.write("\nx\fx\16x\u0349\13x\3x\3x\3x\5x\u034e\nx\3y\3y\5y\u0352")
        buf.write("\ny\3z\3z\3{\3{\3{\3{\5{\u035a\n{\5\u01e3\u033a\u0347")
        buf.write("\2|\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r")
        buf.write("\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30")
        buf.write("/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'")
        buf.write("M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q")
        buf.write("\2s:u;w<y={>}?\177@\u0081A\u0083B\u0085C\u0087D\u0089")
        buf.write("E\u008bF\u008dG\u008fH\u0091I\u0093J\u0095K\u0097L\u0099")
        buf.write("M\u009bN\u009dO\u009fP\u00a1Q\u00a3R\u00a5S\u00a7T\u00a9")
        buf.write("U\u00abV\u00adW\u00afX\u00b1Y\u00b3Z\u00b5[\u00b7\\\u00b9")
        buf.write("]\u00bb^\u00bd_\u00bf`\u00c1a\u00c3b\u00c5c\u00c7d\u00c9")
        buf.write("e\u00cbf\u00cdg\u00cfh\u00d1i\u00d3j\u00d5k\u00d7l\u00d9")
        buf.write("m\u00db\2\u00ddn\u00dfo\u00e1p\u00e3q\u00e5r\u00e7s\u00e9")
        buf.write("t\u00ebu\u00ed\2\u00ef\2\u00f1\2\u00f3\2\u00f5\2\3\2\13")
        buf.write("\4\2\f\f\16\17\3\2\62;\5\2C\\aac|\6\2\62;C\\aac|\3\2\60")
        buf.write("\60\5\2\62;CHch\6\2\f\f\16\17))^^\6\2\f\f\16\17$$^^\3")
        buf.write("\2^^\2\u036d\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3")
        buf.write("\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2")
        buf.write("\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2")
        buf.write("\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2")
        buf.write("#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2")
        buf.write("\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65")
        buf.write("\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2")
        buf.write("\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2")
        buf.write("\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2")
        buf.write("\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3")
        buf.write("\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e")
        buf.write("\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2")
        buf.write("o\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2")
        buf.write("\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2")
        buf.write("\u0083\3\2\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089")
        buf.write("\3\2\2\2\2\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f\3\2\2")
        buf.write("\2\2\u0091\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2\2\2\u0097")
        buf.write("\3\2\2\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d\3\2\2")
        buf.write("\2\2\u009f\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2\2\2\u00a5")
        buf.write("\3\2\2\2\2\u00a7\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab\3\2\2")
        buf.write("\2\2\u00ad\3\2\2\2\2\u00af\3\2\2\2\2\u00b1\3\2\2\2\2\u00b3")
        buf.write("\3\2\2\2\2\u00b5\3\2\2\2\2\u00b7\3\2\2\2\2\u00b9\3\2\2")
        buf.write("\2\2\u00bb\3\2\2\2\2\u00bd\3\2\2\2\2\u00bf\3\2\2\2\2\u00c1")
        buf.write("\3\2\2\2\2\u00c3\3\2\2\2\2\u00c5\3\2\2\2\2\u00c7\3\2\2")
        buf.write("\2\2\u00c9\3\2\2\2\2\u00cb\3\2\2\2\2\u00cd\3\2\2\2\2\u00cf")
        buf.write("\3\2\2\2\2\u00d1\3\2\2\2\2\u00d3\3\2\2\2\2\u00d5\3\2\2")
        buf.write("\2\2\u00d7\3\2\2\2\2\u00d9\3\2\2\2\2\u00dd\3\2\2\2\2\u00df")
        buf.write("\3\2\2\2\2\u00e1\3\2\2\2\2\u00e3\3\2\2\2\2\u00e5\3\2\2")
        buf.write("\2\2\u00e7\3\2\2\2\2\u00e9\3\2\2\2\2\u00eb\3\2\2\2\3\u00f7")
        buf.write("\3\2\2\2\5\u00fb\3\2\2\2\7\u00ff\3\2\2\2\t\u0102\3\2\2")
        buf.write("\2\13\u0105\3\2\2\2\r\u0107\3\2\2\2\17\u0109\3\2\2\2\21")
        buf.write("\u010b\3\2\2\2\23\u010d\3\2\2\2\25\u010f\3\2\2\2\27\u0112")
        buf.write("\3\2\2\2\31\u0114\3\2\2\2\33\u0116\3\2\2\2\35\u011a\3")
        buf.write("\2\2\2\37\u011d\3\2\2\2!\u0120\3\2\2\2#\u0123\3\2\2\2")
        buf.write("%\u0126\3\2\2\2\'\u0129\3\2\2\2)\u012b\3\2\2\2+\u012e")
        buf.write("\3\2\2\2-\u0130\3\2\2\2/\u0133\3\2\2\2\61\u0135\3\2\2")
        buf.write("\2\63\u0139\3\2\2\2\65\u013d\3\2\2\2\67\u0141\3\2\2\2")
        buf.write("9\u0149\3\2\2\2;\u0154\3\2\2\2=\u015b\3\2\2\2?\u0164\3")
        buf.write("\2\2\2A\u0170\3\2\2\2C\u0174\3\2\2\2E\u0178\3\2\2\2G\u017d")
        buf.write("\3\2\2\2I\u0182\3\2\2\2K\u0186\3\2\2\2M\u018a\3\2\2\2")
        buf.write("O\u018e\3\2\2\2Q\u0193\3\2\2\2S\u0197\3\2\2\2U\u019b\3")
        buf.write("\2\2\2W\u019e\3\2\2\2Y\u01a1\3\2\2\2[\u01a4\3\2\2\2]\u01a7")
        buf.write("\3\2\2\2_\u01aa\3\2\2\2a\u01ad\3\2\2\2c\u01b0\3\2\2\2")
        buf.write("e\u01b4\3\2\2\2g\u01b7\3\2\2\2i\u01bc\3\2\2\2k\u01c0\3")
        buf.write("\2\2\2m\u01c5\3\2\2\2o\u01db\3\2\2\2q\u01ef\3\2\2\2s\u01f1")
        buf.write("\3\2\2\2u\u01f3\3\2\2\2w\u01f6\3\2\2\2y\u01f9\3\2\2\2")
        buf.write("{\u01fb\3\2\2\2}\u01fd\3\2\2\2\177\u0200\3\2\2\2\u0081")
        buf.write("\u0202\3\2\2\2\u0083\u0209\3\2\2\2\u0085\u020f\3\2\2\2")
        buf.write("\u0087\u0214\3\2\2\2\u0089\u0217\3\2\2\2\u008b\u0223\3")
        buf.write("\2\2\2\u008d\u0226\3\2\2\2\u008f\u022b\3\2\2\2\u0091\u0232")
        buf.write("\3\2\2\2\u0093\u0234\3\2\2\2\u0095\u0238\3\2\2\2\u0097")
        buf.write("\u023a\3\2\2\2\u0099\u0240\3\2\2\2\u009b\u0246\3\2\2\2")
        buf.write("\u009d\u024d\3\2\2\2\u009f\u0251\3\2\2\2\u00a1\u0256\3")
        buf.write("\2\2\2\u00a3\u025f\3\2\2\2\u00a5\u0264\3\2\2\2\u00a7\u0268")
        buf.write("\3\2\2\2\u00a9\u026e\3\2\2\2\u00ab\u0278\3\2\2\2\u00ad")
        buf.write("\u027b\3\2\2\2\u00af\u0286\3\2\2\2\u00b1\u028b\3\2\2\2")
        buf.write("\u00b3\u028f\3\2\2\2\u00b5\u0292\3\2\2\2\u00b7\u0297\3")
        buf.write("\2\2\2\u00b9\u029c\3\2\2\2\u00bb\u029e\3\2\2\2\u00bd\u02a4")
        buf.write("\3\2\2\2\u00bf\u02a8\3\2\2\2\u00c1\u02af\3\2\2\2\u00c3")
        buf.write("\u02b5\3\2\2\2\u00c5\u02b7\3\2\2\2\u00c7\u02bd\3\2\2\2")
        buf.write("\u00c9\u02c2\3\2\2\2\u00cb\u02c4\3\2\2\2\u00cd\u02c9\3")
        buf.write("\2\2\2\u00cf\u02dd\3\2\2\2\u00d1\u02df\3\2\2\2\u00d3\u02ef")
        buf.write("\3\2\2\2\u00d5\u02f1\3\2\2\2\u00d7\u02f8\3\2\2\2\u00d9")
        buf.write("\u02fd\3\2\2\2\u00db\u0305\3\2\2\2\u00dd\u0307\3\2\2\2")
        buf.write("\u00df\u030a\3\2\2\2\u00e1\u030d\3\2\2\2\u00e3\u0310\3")
        buf.write("\2\2\2\u00e5\u0313\3\2\2\2\u00e7\u0316\3\2\2\2\u00e9\u0319")
        buf.write("\3\2\2\2\u00eb\u031d\3\2\2\2\u00ed\u0331\3\2\2\2\u00ef")
        buf.write("\u034d\3\2\2\2\u00f1\u0351\3\2\2\2\u00f3\u0353\3\2\2\2")
        buf.write("\u00f5\u0359\3\2\2\2\u00f7\u00f8\7\60\2\2\u00f8\u00f9")
        buf.write("\7\60\2\2\u00f9\u00fa\7\60\2\2\u00fa\4\3\2\2\2\u00fb\u00fc")
        buf.write("\7c\2\2\u00fc\u00fd\7p\2\2\u00fd\u00fe\7f\2\2\u00fe\6")
        buf.write("\3\2\2\2\u00ff\u0100\7q\2\2\u0100\u0101\7t\2\2\u0101\b")
        buf.write("\3\2\2\2\u0102\u0103\7?\2\2\u0103\u0104\7@\2\2\u0104\n")
        buf.write("\3\2\2\2\u0105\u0106\7(\2\2\u0106\f\3\2\2\2\u0107\u0108")
        buf.write("\7~\2\2\u0108\16\3\2\2\2\u0109\u010a\7`\2\2\u010a\20\3")
        buf.write("\2\2\2\u010b\u010c\7/\2\2\u010c\22\3\2\2\2\u010d\u010e")
        buf.write("\7-\2\2\u010e\24\3\2\2\2\u010f\u0110\7\61\2\2\u0110\u0111")
        buf.write("\7\61\2\2\u0111\26\3\2\2\2\u0112\u0113\7\61\2\2\u0113")
        buf.write("\30\3\2\2\2\u0114\u0115\7\'\2\2\u0115\32\3\2\2\2\u0116")
        buf.write("\u0117\7o\2\2\u0117\u0118\7q\2\2\u0118\u0119\7f\2\2\u0119")
        buf.write("\34\3\2\2\2\u011a\u011b\7,\2\2\u011b\u011c\7,\2\2\u011c")
        buf.write("\36\3\2\2\2\u011d\u011e\7>\2\2\u011e\u011f\7>\2\2\u011f")
        buf.write(" \3\2\2\2\u0120\u0121\7@\2\2\u0121\u0122\7@\2\2\u0122")
        buf.write("\"\3\2\2\2\u0123\u0124\7?\2\2\u0124\u0125\7?\2\2\u0125")
        buf.write("$\3\2\2\2\u0126\u0127\7#\2\2\u0127\u0128\7?\2\2\u0128")
        buf.write("&\3\2\2\2\u0129\u012a\7>\2\2\u012a(\3\2\2\2\u012b\u012c")
        buf.write("\7>\2\2\u012c\u012d\7?\2\2\u012d*\3\2\2\2\u012e\u012f")
        buf.write("\7@\2\2\u012f,\3\2\2\2\u0130\u0131\7@\2\2\u0131\u0132")
        buf.write("\7?\2\2\u0132.\3\2\2\2\u0133\u0134\7\u0080\2\2\u0134\60")
        buf.write("\3\2\2\2\u0135\u0136\7c\2\2\u0136\u0137\7d\2\2\u0137\u0138")
        buf.write("\7u\2\2\u0138\62\3\2\2\2\u0139\u013a\7c\2\2\u013a\u013b")
        buf.write("\7n\2\2\u013b\u013c\7n\2\2\u013c\64\3\2\2\2\u013d\u013e")
        buf.write("\7c\2\2\u013e\u013f\7p\2\2\u013f\u0140\7{\2\2\u0140\66")
        buf.write("\3\2\2\2\u0141\u0142\7c\2\2\u0142\u0143\7v\2\2\u0143\u0144")
        buf.write("\7N\2\2\u0144\u0145\7c\2\2\u0145\u0146\7d\2\2\u0146\u0147")
        buf.write("\7g\2\2\u0147\u0148\7n\2\2\u01488\3\2\2\2\u0149\u014a")
        buf.write("\7e\2\2\u014a\u014b\7q\2\2\u014b\u014c\7w\2\2\u014c\u014d")
        buf.write("\7p\2\2\u014d\u014e\7v\2\2\u014e\u014f\7N\2\2\u014f\u0150")
        buf.write("\7c\2\2\u0150\u0151\7d\2\2\u0151\u0152\7g\2\2\u0152\u0153")
        buf.write("\7n\2\2\u0153:\3\2\2\2\u0154\u0155\7e\2\2\u0155\u0156")
        buf.write("\7j\2\2\u0156\u0157\7q\2\2\u0157\u0158\7q\2\2\u0158\u0159")
        buf.write("\7u\2\2\u0159\u015a\7g\2\2\u015a<\3\2\2\2\u015b\u015c")
        buf.write("\7e\2\2\u015c\u015d\7q\2\2\u015d\u015e\7p\2\2\u015e\u015f")
        buf.write("\7v\2\2\u015f\u0160\7g\2\2\u0160\u0161\7z\2\2\u0161\u0162")
        buf.write("\7v\2\2\u0162\u0163\7u\2\2\u0163>\3\2\2\2\u0164\u0165")
        buf.write("\7i\2\2\u0165\u0166\7g\2\2\u0166\u0167\7v\2\2\u0167\u0168")
        buf.write("\7a\2\2\u0168\u0169\7e\2\2\u0169\u016a\7q\2\2\u016a\u016b")
        buf.write("\7p\2\2\u016b\u016c\7v\2\2\u016c\u016d\7g\2\2\u016d\u016e")
        buf.write("\7z\2\2\u016e\u016f\7v\2\2\u016f@\3\2\2\2\u0170\u0171")
        buf.write("\7o\2\2\u0171\u0172\7k\2\2\u0172\u0173\7p\2\2\u0173B\3")
        buf.write("\2\2\2\u0174\u0175\7o\2\2\u0175\u0176\7c\2\2\u0176\u0177")
        buf.write("\7z\2\2\u0177D\3\2\2\2\u0178\u0179\7m\2\2\u0179\u017a")
        buf.write("\7g\2\2\u017a\u017b\7{\2\2\u017b\u017c\7u\2\2\u017cF\3")
        buf.write("\2\2\2\u017d\u017e\7j\2\2\u017e\u017f\7c\2\2\u017f\u0180")
        buf.write("\7u\2\2\u0180\u0181\7j\2\2\u0181H\3\2\2\2\u0182\u0183")
        buf.write("\7n\2\2\u0183\u0184\7g\2\2\u0184\u0185\7p\2\2\u0185J\3")
        buf.write("\2\2\2\u0186\u0187\7u\2\2\u0187\u0188\7v\2\2\u0188\u0189")
        buf.write("\7t\2\2\u0189L\3\2\2\2\u018a\u018b\7g\2\2\u018b\u018c")
        buf.write("\7p\2\2\u018c\u018d\7f\2\2\u018dN\3\2\2\2\u018e\u018f")
        buf.write("\7c\2\2\u018f\u0190\7p\2\2\u0190\u0191\7f\2\2\u0191\u0192")
        buf.write("\7?\2\2\u0192P\3\2\2\2\u0193\u0194\7q\2\2\u0194\u0195")
        buf.write("\7t\2\2\u0195\u0196\7?\2\2\u0196R\3\2\2\2\u0197\u0198")
        buf.write("\7?\2\2\u0198\u0199\7@\2\2\u0199\u019a\7?\2\2\u019aT\3")
        buf.write("\2\2\2\u019b\u019c\7(\2\2\u019c\u019d\7?\2\2\u019dV\3")
        buf.write("\2\2\2\u019e\u019f\7~\2\2\u019f\u01a0\7?\2\2\u01a0X\3")
        buf.write("\2\2\2\u01a1\u01a2\7`\2\2\u01a2\u01a3\7?\2\2\u01a3Z\3")
        buf.write("\2\2\2\u01a4\u01a5\7/\2\2\u01a5\u01a6\7?\2\2\u01a6\\\3")
        buf.write("\2\2\2\u01a7\u01a8\7-\2\2\u01a8\u01a9\7?\2\2\u01a9^\3")
        buf.write("\2\2\2\u01aa\u01ab\7,\2\2\u01ab\u01ac\7?\2\2\u01ac`\3")
        buf.write("\2\2\2\u01ad\u01ae\7\61\2\2\u01ae\u01af\7?\2\2\u01afb")
        buf.write("\3\2\2\2\u01b0\u01b1\7\61\2\2\u01b1\u01b2\7\61\2\2\u01b2")
        buf.write("\u01b3\7?\2\2\u01b3d\3\2\2\2\u01b4\u01b5\7\'\2\2\u01b5")
        buf.write("\u01b6\7?\2\2\u01b6f\3\2\2\2\u01b7\u01b8\7o\2\2\u01b8")
        buf.write("\u01b9\7q\2\2\u01b9\u01ba\7f\2\2\u01ba\u01bb\7?\2\2\u01bb")
        buf.write("h\3\2\2\2\u01bc\u01bd\7,\2\2\u01bd\u01be\7,\2\2\u01be")
        buf.write("\u01bf\7?\2\2\u01bfj\3\2\2\2\u01c0\u01c1\7@\2\2\u01c1")
        buf.write("\u01c2\7@\2\2\u01c2\u01c3\7?\2\2\u01c3l\3\2\2\2\u01c4")
        buf.write("\u01c6\7\17\2\2\u01c5\u01c4\3\2\2\2\u01c5\u01c6\3\2\2")
        buf.write("\2\u01c6\u01c7\3\2\2\2\u01c7\u01cf\7\f\2\2\u01c8\u01ca")
        buf.write("\7\"\2\2\u01c9\u01c8\3\2\2\2\u01ca\u01cd\3\2\2\2\u01cb")
        buf.write("\u01c9\3\2\2\2\u01cb\u01cc\3\2\2\2\u01cc\u01d0\3\2\2\2")
        buf.write("\u01cd\u01cb\3\2\2\2\u01ce\u01d0\7\13\2\2\u01cf\u01cb")
        buf.write("\3\2\2\2\u01cf\u01ce\3\2\2\2\u01d0\u01d1\3\2\2\2\u01d1")
        buf.write("\u01d2\b\67\2\2\u01d2n\3\2\2\2\u01d3\u01d5\7\"\2\2\u01d4")
        buf.write("\u01d3\3\2\2\2\u01d5\u01d6\3\2\2\2\u01d6\u01d4\3\2\2\2")
        buf.write("\u01d6\u01d7\3\2\2\2\u01d7\u01dc\3\2\2\2\u01d8\u01d9\7")
        buf.write("^\2\2\u01d9\u01dc\5m\67\2\u01da\u01dc\5q9\2\u01db\u01d4")
        buf.write("\3\2\2\2\u01db\u01d8\3\2\2\2\u01db\u01da\3\2\2\2\u01dc")
        buf.write("\u01dd\3\2\2\2\u01dd\u01de\b8\3\2\u01dep\3\2\2\2\u01df")
        buf.write("\u01e3\5u;\2\u01e0\u01e2\13\2\2\2\u01e1\u01e0\3\2\2\2")
        buf.write("\u01e2\u01e5\3\2\2\2\u01e3\u01e4\3\2\2\2\u01e3\u01e1\3")
        buf.write("\2\2\2\u01e4\u01e6\3\2\2\2\u01e5\u01e3\3\2\2\2\u01e6\u01e7")
        buf.write("\5w<\2\u01e7\u01f0\3\2\2\2\u01e8\u01ec\5s:\2\u01e9\u01eb")
        buf.write("\n\2\2\2\u01ea\u01e9\3\2\2\2\u01eb\u01ee\3\2\2\2\u01ec")
        buf.write("\u01ea\3\2\2\2\u01ec\u01ed\3\2\2\2\u01ed\u01f0\3\2\2\2")
        buf.write("\u01ee\u01ec\3\2\2\2\u01ef\u01df\3\2\2\2\u01ef\u01e8\3")
        buf.write("\2\2\2\u01f0r\3\2\2\2\u01f1\u01f2\7%\2\2\u01f2t\3\2\2")
        buf.write("\2\u01f3\u01f4\7*\2\2\u01f4\u01f5\7,\2\2\u01f5v\3\2\2")
        buf.write("\2\u01f6\u01f7\7,\2\2\u01f7\u01f8\7+\2\2\u01f8x\3\2\2")
        buf.write("\2\u01f9\u01fa\7#\2\2\u01faz\3\2\2\2\u01fb\u01fc\7,\2")
        buf.write("\2\u01fc|\3\2\2\2\u01fd\u01fe\7c\2\2\u01fe\u01ff\7u\2")
        buf.write("\2\u01ff~\3\2\2\2\u0200\u0201\7\60\2\2\u0201\u0080\3\2")
        buf.write("\2\2\u0202\u0203\7k\2\2\u0203\u0204\7o\2\2\u0204\u0205")
        buf.write("\7r\2\2\u0205\u0206\7q\2\2\u0206\u0207\7t\2\2\u0207\u0208")
        buf.write("\7v\2\2\u0208\u0082\3\2\2\2\u0209\u020a\7r\2\2\u020a\u020b")
        buf.write("\7t\2\2\u020b\u020c\7k\2\2\u020c\u020d\7p\2\2\u020d\u020e")
        buf.write("\7v\2\2\u020e\u0084\3\2\2\2\u020f\u0210\7h\2\2\u0210\u0211")
        buf.write("\7t\2\2\u0211\u0212\7q\2\2\u0212\u0213\7o\2\2\u0213\u0086")
        buf.write("\3\2\2\2\u0214\u0215\7\60\2\2\u0215\u0216\7\60\2\2\u0216")
        buf.write("\u0088\3\2\2\2\u0217\u0218\7u\2\2\u0218\u0219\7g\2\2\u0219")
        buf.write("\u021a\7v\2\2\u021a\u021b\7k\2\2\u021b\u021c\7p\2\2\u021c")
        buf.write("\u021d\7v\2\2\u021d\u021e\7n\2\2\u021e\u021f\7g\2\2\u021f")
        buf.write("\u0220\7x\2\2\u0220\u0221\7g\2\2\u0221\u0222\7n\2\2\u0222")
        buf.write("\u008a\3\2\2\2\u0223\u0224\7/\2\2\u0224\u0225\7@\2\2\u0225")
        buf.write("\u008c\3\2\2\2\u0226\u0227\7u\2\2\u0227\u0228\7v\2\2\u0228")
        buf.write("\u0229\7q\2\2\u0229\u022a\7r\2\2\u022a\u008e\3\2\2\2\u022b")
        buf.write("\u022c\7n\2\2\u022c\u022d\7c\2\2\u022d\u022e\7o\2\2\u022e")
        buf.write("\u022f\7d\2\2\u022f\u0230\7f\2\2\u0230\u0231\7c\2\2\u0231")
        buf.write("\u0090\3\2\2\2\u0232\u0233\7A\2\2\u0233\u0092\3\2\2\2")
        buf.write("\u0234\u0235\7p\2\2\u0235\u0236\7q\2\2\u0236\u0237\7v")
        buf.write("\2\2\u0237\u0094\3\2\2\2\u0238\u0239\7.\2\2\u0239\u0096")
        buf.write("\3\2\2\2\u023a\u023b\7e\2\2\u023b\u023c\7q\2\2\u023c\u023d")
        buf.write("\7p\2\2\u023d\u023e\7u\2\2\u023e\u023f\7v\2\2\u023f\u0098")
        buf.write("\3\2\2\2\u0240\u0241\7c\2\2\u0241\u0242\7y\2\2\u0242\u0243")
        buf.write("\7c\2\2\u0243\u0244\7k\2\2\u0244\u0245\7v\2\2\u0245\u009a")
        buf.write("\3\2\2\2\u0246\u0247\7c\2\2\u0247\u0248\7u\2\2\u0248\u0249")
        buf.write("\7u\2\2\u0249\u024a\7g\2\2\u024a\u024b\7t\2\2\u024b\u024c")
        buf.write("\7v\2\2\u024c\u009c\3\2\2\2\u024d\u024e\7x\2\2\u024e\u024f")
        buf.write("\7c\2\2\u024f\u0250\7t\2\2\u0250\u009e\3\2\2\2\u0251\u0252")
        buf.write("\7v\2\2\u0252\u0253\7t\2\2\u0253\u0254\7c\2\2\u0254\u0255")
        buf.write("\7r\2\2\u0255\u00a0\3\2\2\2\u0256\u0257\7r\2\2\u0257\u0258")
        buf.write("\7q\2\2\u0258\u0259\7u\2\2\u0259\u025a\7u\2\2\u025a\u025b")
        buf.write("\7k\2\2\u025b\u025c\7d\2\2\u025c\u025d\7n\2\2\u025d\u025e")
        buf.write("\7{\2\2\u025e\u00a2\3\2\2\2\u025f\u0260\7r\2\2\u0260\u0261")
        buf.write("\7c\2\2\u0261\u0262\7u\2\2\u0262\u0263\7u\2\2\u0263\u00a4")
        buf.write("\3\2\2\2\u0264\u0265\7f\2\2\u0265\u0266\7g\2\2\u0266\u0267")
        buf.write("\7n\2\2\u0267\u00a6\3\2\2\2\u0268\u0269\7u\2\2\u0269\u026a")
        buf.write("\7r\2\2\u026a\u026b\7c\2\2\u026b\u026c\7y\2\2\u026c\u026d")
        buf.write("\7p\2\2\u026d\u00a8\3\2\2\2\u026e\u026f\7k\2\2\u026f\u0270")
        buf.write("\7p\2\2\u0270\u0271\7x\2\2\u0271\u0272\7c\2\2\u0272\u0273")
        buf.write("\7t\2\2\u0273\u0274\7k\2\2\u0274\u0275\7c\2\2\u0275\u0276")
        buf.write("\7p\2\2\u0276\u0277\7v\2\2\u0277\u00aa\3\2\2\2\u0278\u0279")
        buf.write("\7i\2\2\u0279\u027a\7q\2\2\u027a\u00ac\3\2\2\2\u027b\u027c")
        buf.write("\7u\2\2\u027c\u027d\7g\2\2\u027d\u027e\7s\2\2\u027e\u027f")
        buf.write("\7w\2\2\u027f\u0280\7g\2\2\u0280\u0281\7p\2\2\u0281\u0282")
        buf.write("\7v\2\2\u0282\u0283\7k\2\2\u0283\u0284\7c\2\2\u0284\u0285")
        buf.write("\7n\2\2\u0285\u00ae\3\2\2\2\u0286\u0287\7y\2\2\u0287\u0288")
        buf.write("\7j\2\2\u0288\u0289\7g\2\2\u0289\u028a\7p\2\2\u028a\u00b0")
        buf.write("\3\2\2\2\u028b\u028c\7n\2\2\u028c\u028d\7g\2\2\u028d\u028e")
        buf.write("\7v\2\2\u028e\u00b2\3\2\2\2\u028f\u0290\7k\2\2\u0290\u0291")
        buf.write("\7h\2\2\u0291\u00b4\3\2\2\2\u0292\u0293\7g\2\2\u0293\u0294")
        buf.write("\7n\2\2\u0294\u0295\7k\2\2\u0295\u0296\7h\2\2\u0296\u00b6")
        buf.write("\3\2\2\2\u0297\u0298\7g\2\2\u0298\u0299\7n\2\2\u0299\u029a")
        buf.write("\7u\2\2\u029a\u029b\7g\2\2\u029b\u00b8\3\2\2\2\u029c\u029d")
        buf.write("\7B\2\2\u029d\u00ba\3\2\2\2\u029e\u029f\7y\2\2\u029f\u02a0")
        buf.write("\7j\2\2\u02a0\u02a1\7k\2\2\u02a1\u02a2\7n\2\2\u02a2\u02a3")
        buf.write("\7g\2\2\u02a3\u00bc\3\2\2\2\u02a4\u02a5\7f\2\2\u02a5\u02a6")
        buf.write("\7g\2\2\u02a6\u02a7\7h\2\2\u02a7\u00be\3\2\2\2\u02a8\u02a9")
        buf.write("\7g\2\2\u02a9\u02aa\7z\2\2\u02aa\u02ab\7k\2\2\u02ab\u02ac")
        buf.write("\7u\2\2\u02ac\u02ad\7v\2\2\u02ad\u02ae\7u\2\2\u02ae\u00c0")
        buf.write("\3\2\2\2\u02af\u02b0\7y\2\2\u02b0\u02b1\7j\2\2\u02b1\u02b2")
        buf.write("\7g\2\2\u02b2\u02b3\7t\2\2\u02b3\u02b4\7g\2\2\u02b4\u00c2")
        buf.write("\3\2\2\2\u02b5\u02b6\7?\2\2\u02b6\u00c4\3\2\2\2\u02b7")
        buf.write("\u02b8\7h\2\2\u02b8\u02b9\7q\2\2\u02b9\u02ba\7t\2\2\u02ba")
        buf.write("\u02bb\3\2\2\2\u02bb\u02bc\bc\4\2\u02bc\u00c6\3\2\2\2")
        buf.write("\u02bd\u02be\7k\2\2\u02be\u02bf\7p\2\2\u02bf\u02c0\3\2")
        buf.write("\2\2\u02c0\u02c1\bd\5\2\u02c1\u00c8\3\2\2\2\u02c2\u02c3")
        buf.write("\7<\2\2\u02c3\u00ca\3\2\2\2\u02c4\u02c5\7P\2\2\u02c5\u02c6")
        buf.write("\7q\2\2\u02c6\u02c7\7p\2\2\u02c7\u02c8\7g\2\2\u02c8\u00cc")
        buf.write("\3\2\2\2\u02c9\u02ca\7c\2\2\u02ca\u02cb\7v\2\2\u02cb\u02cc")
        buf.write("\7q\2\2\u02cc\u02cd\7o\2\2\u02cd\u02ce\7k\2\2\u02ce\u02cf")
        buf.write("\7e\2\2\u02cf\u02d0\7c\2\2\u02d0\u02d1\7n\2\2\u02d1\u02d2")
        buf.write("\7n\2\2\u02d2\u02d3\7{\2\2\u02d3\u00ce\3\2\2\2\u02d4\u02d5")
        buf.write("\7H\2\2\u02d5\u02d6\7c\2\2\u02d6\u02d7\7n\2\2\u02d7\u02d8")
        buf.write("\7u\2\2\u02d8\u02de\7g\2\2\u02d9\u02da\7V\2\2\u02da\u02db")
        buf.write("\7t\2\2\u02db\u02dc\7w\2\2\u02dc\u02de\7g\2\2\u02dd\u02d4")
        buf.write("\3\2\2\2\u02dd\u02d9\3\2\2\2\u02de\u00d0\3\2\2\2\u02df")
        buf.write("\u02e0\7g\2\2\u02e0\u02e1\7v\2\2\u02e1\u02e2\7g\2\2\u02e2")
        buf.write("\u02e3\7t\2\2\u02e3\u02e4\7p\2\2\u02e4\u02e5\7c\2\2\u02e5")
        buf.write("\u02e6\7n\2\2\u02e6\u00d2\3\2\2\2\u02e7\u02e9\t\3\2\2")
        buf.write("\u02e8\u02e7\3\2\2\2\u02e9\u02ea\3\2\2\2\u02ea\u02e8\3")
        buf.write("\2\2\2\u02ea\u02eb\3\2\2\2\u02eb\u02f0\3\2\2\2\u02ec\u02ed")
        buf.write("\7k\2\2\u02ed\u02ee\7p\2\2\u02ee\u02f0\7h\2\2\u02ef\u02e8")
        buf.write("\3\2\2\2\u02ef\u02ec\3\2\2\2\u02f0\u00d4\3\2\2\2\u02f1")
        buf.write("\u02f5\t\4\2\2\u02f2\u02f4\t\5\2\2\u02f3\u02f2\3\2\2\2")
        buf.write("\u02f4\u02f7\3\2\2\2\u02f5\u02f3\3\2\2\2\u02f5\u02f6\3")
        buf.write("\2\2\2\u02f6\u00d6\3\2\2\2\u02f7\u02f5\3\2\2\2\u02f8\u02fb")
        buf.write("\t\6\2\2\u02f9\u02fc\5\u00d9m\2\u02fa\u02fc\5\u00d5k\2")
        buf.write("\u02fb\u02f9\3\2\2\2\u02fb\u02fa\3\2\2\2\u02fc\u00d8\3")
        buf.write("\2\2\2\u02fd\u02fe\7\62\2\2\u02fe\u02ff\7Z\2\2\u02ff\u0301")
        buf.write("\3\2\2\2\u0300\u0302\5\u00dbn\2\u0301\u0300\3\2\2\2\u0302")
        buf.write("\u0303\3\2\2\2\u0303\u0301\3\2\2\2\u0303\u0304\3\2\2\2")
        buf.write("\u0304\u00da\3\2\2\2\u0305\u0306\t\7\2\2\u0306\u00dc\3")
        buf.write("\2\2\2\u0307\u0308\7]\2\2\u0308\u0309\bo\6\2\u0309\u00de")
        buf.write("\3\2\2\2\u030a\u030b\7_\2\2\u030b\u030c\bp\7\2\u030c\u00e0")
        buf.write("\3\2\2\2\u030d\u030e\7}\2\2\u030e\u030f\bq\b\2\u030f\u00e2")
        buf.write("\3\2\2\2\u0310\u0311\7\177\2\2\u0311\u0312\br\t\2\u0312")
        buf.write("\u00e4\3\2\2\2\u0313\u0314\7*\2\2\u0314\u0315\bs\n\2\u0315")
        buf.write("\u00e6\3\2\2\2\u0316\u0317\7+\2\2\u0317\u0318\bt\13\2")
        buf.write("\u0318\u00e8\3\2\2\2\u0319\u031a\7=\2\2\u031a\u00ea\3")
        buf.write("\2\2\2\u031b\u031e\5\u00edw\2\u031c\u031e\5\u00efx\2\u031d")
        buf.write("\u031b\3\2\2\2\u031d\u031c\3\2\2\2\u031e\u00ec\3\2\2\2")
        buf.write("\u031f\u0324\7)\2\2\u0320\u0323\5\u00f5{\2\u0321\u0323")
        buf.write("\n\b\2\2\u0322\u0320\3\2\2\2\u0322\u0321\3\2\2\2\u0323")
        buf.write("\u0326\3\2\2\2\u0324\u0322\3\2\2\2\u0324\u0325\3\2\2\2")
        buf.write("\u0325\u0327\3\2\2\2\u0326\u0324\3\2\2\2\u0327\u0332\7")
        buf.write(")\2\2\u0328\u032d\7$\2\2\u0329\u032c\5\u00f5{\2\u032a")
        buf.write("\u032c\n\t\2\2\u032b\u0329\3\2\2\2\u032b\u032a\3\2\2\2")
        buf.write("\u032c\u032f\3\2\2\2\u032d\u032b\3\2\2\2\u032d\u032e\3")
        buf.write("\2\2\2\u032e\u0330\3\2\2\2\u032f\u032d\3\2\2\2\u0330\u0332")
        buf.write("\7$\2\2\u0331\u031f\3\2\2\2\u0331\u0328\3\2\2\2\u0332")
        buf.write("\u00ee\3\2\2\2\u0333\u0334\7)\2\2\u0334\u0335\7)\2\2\u0335")
        buf.write("\u0336\7)\2\2\u0336\u033a\3\2\2\2\u0337\u0339\5\u00f1")
        buf.write("y\2\u0338\u0337\3\2\2\2\u0339\u033c\3\2\2\2\u033a\u033b")
        buf.write("\3\2\2\2\u033a\u0338\3\2\2\2\u033b\u033d\3\2\2\2\u033c")
        buf.write("\u033a\3\2\2\2\u033d\u033e\7)\2\2\u033e\u033f\7)\2\2\u033f")
        buf.write("\u034e\7)\2\2\u0340\u0341\7$\2\2\u0341\u0342\7$\2\2\u0342")
        buf.write("\u0343\7$\2\2\u0343\u0347\3\2\2\2\u0344\u0346\5\u00f1")
        buf.write("y\2\u0345\u0344\3\2\2\2\u0346\u0349\3\2\2\2\u0347\u0348")
        buf.write("\3\2\2\2\u0347\u0345\3\2\2\2\u0348\u034a\3\2\2\2\u0349")
        buf.write("\u0347\3\2\2\2\u034a\u034b\7$\2\2\u034b\u034c\7$\2\2\u034c")
        buf.write("\u034e\7$\2\2\u034d\u0333\3\2\2\2\u034d\u0340\3\2\2\2")
        buf.write("\u034e\u00f0\3\2\2\2\u034f\u0352\5\u00f3z\2\u0350\u0352")
        buf.write("\5\u00f5{\2\u0351\u034f\3\2\2\2\u0351\u0350\3\2\2\2\u0352")
        buf.write("\u00f2\3\2\2\2\u0353\u0354\n\n\2\2\u0354\u00f4\3\2\2\2")
        buf.write("\u0355\u0356\7^\2\2\u0356\u035a\13\2\2\2\u0357\u0358\7")
        buf.write("^\2\2\u0358\u035a\5m\67\2\u0359\u0355\3\2\2\2\u0359\u0357")
        buf.write("\3\2\2\2\u035a\u00f6\3\2\2\2\34\2\u01c5\u01cb\u01cf\u01d6")
        buf.write("\u01db\u01e3\u01ec\u01ef\u02dd\u02ea\u02ef\u02f5\u02fb")
        buf.write("\u0303\u031d\u0322\u0324\u032b\u032d\u0331\u033a\u0347")
        buf.write("\u034d\u0351\u0359\f\3\67\2\b\2\2\3c\3\3d\4\3o\5\3p\6")
        buf.write("\3q\7\3r\b\3s\t\3t\n")
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


    class HarmonyDenter(ModifiedDenterHelper):
        def __init__(self, lexer, nl_token, colon_token, indent_token, dedent_token, ignore_eof):
            super().__init__(nl_token, colon_token, indent_token, dedent_token, ignore_eof)
            self.lexer: HarmonyLexer = lexer

        def pull_token(self):
            return super(HarmonyLexer, self.lexer).nextToken()

    @property
    def opened_for(self):
        try:
            return self._opened_for
        except AttributeError:
            self._opened_for = 0
            return self._opened_for

    @opened_for.setter
    def opened_for(self, value):
        self._opened_for = value

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
            self.denter = self.HarmonyDenter(self, self.NL, self.COLON, HarmonyParser.INDENT, HarmonyParser.DEDENT, ignore_eof=False)
        token = self.denter.next_token()
        return token


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[53] = self.NL_action 
            actions[97] = self.FOR_action 
            actions[98] = self.IN_action 
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

            if self.opened or self.opened_for:
                self.skip()

     

    def FOR_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            self.opened_for += 1
     

    def IN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:

            if self.opened_for >= 0:
                self.opened_for -= 1

     

    def OPEN_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:
            self.opened += 1
     

    def CLOSE_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:
            self.opened -= 1
     

    def OPEN_BRACES_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 5:
            self.opened += 1
     

    def CLOSE_BRACES_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 6:
            self.opened -= 1
     

    def OPEN_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 7:
            self.opened += 1
     

    def CLOSE_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 8:
            self.opened -= 1
     


