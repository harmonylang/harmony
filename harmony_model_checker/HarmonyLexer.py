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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2v")
        buf.write("\u035e\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("y\ty\4z\tz\4{\t{\4|\t|\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3")
        buf.write("\3\4\3\4\3\4\3\5\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3")
        buf.write("\t\3\n\3\n\3\13\3\13\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3")
        buf.write("\16\3\16\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\22\3\22\3\22\3\23\3\23\3\23\3\24\3\24\3\25\3\25\3\25")
        buf.write("\3\26\3\26\3\27\3\27\3\27\3\30\3\30\3\31\3\31\3\31\3\31")
        buf.write("\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3 ")
        buf.write("\3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3!\3!\3!\3!\3\"\3\"")
        buf.write("\3\"\3\"\3#\3#\3#\3#\3#\3$\3$\3$\3$\3$\3%\3%\3%\3%\3&")
        buf.write("\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3)\3)\3)\3)")
        buf.write("\3*\3*\3*\3+\3+\3+\3,\3,\3,\3-\3-\3-\3.\3.\3.\3/\3/\3")
        buf.write("/\3\60\3\60\3\60\3\61\3\61\3\61\3\61\3\62\3\62\3\62\3")
        buf.write("\63\3\63\3\63\3\63\3\63\3\64\3\64\3\64\3\64\3\65\3\65")
        buf.write("\3\65\3\65\3\66\5\66\u01c4\n\66\3\66\3\66\7\66\u01c8\n")
        buf.write("\66\f\66\16\66\u01cb\13\66\3\66\3\66\3\67\6\67\u01d0\n")
        buf.write("\67\r\67\16\67\u01d1\3\67\3\67\3\67\5\67\u01d7\n\67\3")
        buf.write("\67\3\67\38\38\78\u01dd\n8\f8\168\u01e0\138\38\38\38\3")
        buf.write("8\78\u01e6\n8\f8\168\u01e9\138\58\u01eb\n8\39\39\3:\3")
        buf.write(":\3:\3;\3;\3;\3<\3<\3=\3=\3>\3>\3>\3?\3?\3@\3@\3@\3@\3")
        buf.write("@\3@\3@\3A\3A\3A\3A\3A\3A\3B\3B\3B\3B\3B\3C\3C\3C\3D\3")
        buf.write("D\3D\3D\3D\3E\3E\3E\3E\3E\3E\3E\3E\3E\3E\3E\3E\3F\3F\3")
        buf.write("F\3G\3G\3G\3G\3G\3H\3H\3H\3H\3H\3H\3H\3I\3I\3J\3J\3J\3")
        buf.write("J\3K\3K\3L\3L\3L\3L\3L\3L\3M\3M\3M\3M\3M\3M\3N\3N\3N\3")
        buf.write("N\3N\3N\3N\3O\3O\3O\3O\3P\3P\3P\3P\3P\3Q\3Q\3Q\3Q\3Q\3")
        buf.write("Q\3Q\3Q\3Q\3R\3R\3R\3R\3R\3S\3S\3S\3S\3T\3T\3T\3T\3T\3")
        buf.write("T\3U\3U\3U\3U\3U\3U\3U\3U\3U\3U\3V\3V\3V\3W\3W\3W\3W\3")
        buf.write("W\3W\3W\3W\3W\3W\3W\3X\3X\3X\3X\3X\3X\3X\3Y\3Y\3Y\3Y\3")
        buf.write("Y\3Z\3Z\3Z\3Z\3[\3[\3[\3\\\3\\\3\\\3\\\3\\\3]\3]\3]\3")
        buf.write("]\3]\3^\3^\3_\3_\3_\3_\3_\3_\3`\3`\3`\3`\3a\3a\3a\3a\3")
        buf.write("a\3a\3a\3b\3b\3b\3b\3b\3b\3c\3c\3d\3d\3d\3d\3e\3e\3e\3")
        buf.write("f\3f\3g\3g\3g\3g\3g\3h\3h\3h\3h\3h\3h\3h\3h\3h\3h\3h\3")
        buf.write("i\3i\3i\3i\3i\3i\3i\3i\3i\5i\u02e1\ni\3j\3j\3j\3j\3j\3")
        buf.write("j\3j\3j\3k\6k\u02ec\nk\rk\16k\u02ed\3k\3k\3k\5k\u02f3")
        buf.write("\nk\3l\3l\7l\u02f7\nl\fl\16l\u02fa\13l\3m\3m\3m\5m\u02ff")
        buf.write("\nm\3n\3n\3n\3n\6n\u0305\nn\rn\16n\u0306\3o\3o\3p\3p\3")
        buf.write("p\3q\3q\3q\3r\3r\3r\3s\3s\3s\3t\3t\3t\3u\3u\3u\3v\3v\3")
        buf.write("w\3w\5w\u0321\nw\3x\3x\3x\7x\u0326\nx\fx\16x\u0329\13")
        buf.write("x\3x\3x\3x\3x\7x\u032f\nx\fx\16x\u0332\13x\3x\5x\u0335")
        buf.write("\nx\3y\3y\3y\3y\3y\7y\u033c\ny\fy\16y\u033f\13y\3y\3y")
        buf.write("\3y\3y\3y\3y\3y\3y\7y\u0349\ny\fy\16y\u034c\13y\3y\3y")
        buf.write("\3y\5y\u0351\ny\3z\3z\5z\u0355\nz\3{\3{\3|\3|\3|\3|\5")
        buf.write("|\u035d\n|\5\u01de\u033d\u034a\2}\3\3\5\4\7\5\t\6\13\7")
        buf.write("\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21")
        buf.write("!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67")
        buf.write("\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61")
        buf.write("a\62c\63e\64g\65i\66k\67m8o\2q9s:u;w<y={>}?\177@\u0081")
        buf.write("A\u0083B\u0085C\u0087D\u0089E\u008bF\u008dG\u008fH\u0091")
        buf.write("I\u0093J\u0095K\u0097L\u0099M\u009bN\u009dO\u009fP\u00a1")
        buf.write("Q\u00a3R\u00a5S\u00a7T\u00a9U\u00abV\u00adW\u00afX\u00b1")
        buf.write("Y\u00b3Z\u00b5[\u00b7\\\u00b9]\u00bb^\u00bd_\u00bf`\u00c1")
        buf.write("a\u00c3b\u00c5c\u00c7d\u00c9e\u00cbf\u00cdg\u00cfh\u00d1")
        buf.write("i\u00d3j\u00d5k\u00d7l\u00d9m\u00dbn\u00dd\2\u00dfo\u00e1")
        buf.write("p\u00e3q\u00e5r\u00e7s\u00e9t\u00ebu\u00edv\u00ef\2\u00f1")
        buf.write("\2\u00f3\2\u00f5\2\u00f7\2\3\2\13\4\2\f\f\16\17\3\2\62")
        buf.write(";\5\2C\\aac|\6\2\62;C\\aac|\3\2\60\60\5\2\62;CHch\6\2")
        buf.write("\f\f\16\17))^^\6\2\f\f\16\17$$^^\3\2^^\2\u036f\2\3\3\2")
        buf.write("\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2")
        buf.write("\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2")
        buf.write("\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35")
        buf.write("\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2")
        buf.write("\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2")
        buf.write("\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2")
        buf.write("\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2")
        buf.write("\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2")
        buf.write("\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3")
        buf.write("\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_")
        buf.write("\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2")
        buf.write("i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2")
        buf.write("\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2")
        buf.write("\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085")
        buf.write("\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2\u008b\3\2\2")
        buf.write("\2\2\u008d\3\2\2\2\2\u008f\3\2\2\2\2\u0091\3\2\2\2\2\u0093")
        buf.write("\3\2\2\2\2\u0095\3\2\2\2\2\u0097\3\2\2\2\2\u0099\3\2\2")
        buf.write("\2\2\u009b\3\2\2\2\2\u009d\3\2\2\2\2\u009f\3\2\2\2\2\u00a1")
        buf.write("\3\2\2\2\2\u00a3\3\2\2\2\2\u00a5\3\2\2\2\2\u00a7\3\2\2")
        buf.write("\2\2\u00a9\3\2\2\2\2\u00ab\3\2\2\2\2\u00ad\3\2\2\2\2\u00af")
        buf.write("\3\2\2\2\2\u00b1\3\2\2\2\2\u00b3\3\2\2\2\2\u00b5\3\2\2")
        buf.write("\2\2\u00b7\3\2\2\2\2\u00b9\3\2\2\2\2\u00bb\3\2\2\2\2\u00bd")
        buf.write("\3\2\2\2\2\u00bf\3\2\2\2\2\u00c1\3\2\2\2\2\u00c3\3\2\2")
        buf.write("\2\2\u00c5\3\2\2\2\2\u00c7\3\2\2\2\2\u00c9\3\2\2\2\2\u00cb")
        buf.write("\3\2\2\2\2\u00cd\3\2\2\2\2\u00cf\3\2\2\2\2\u00d1\3\2\2")
        buf.write("\2\2\u00d3\3\2\2\2\2\u00d5\3\2\2\2\2\u00d7\3\2\2\2\2\u00d9")
        buf.write("\3\2\2\2\2\u00db\3\2\2\2\2\u00df\3\2\2\2\2\u00e1\3\2\2")
        buf.write("\2\2\u00e3\3\2\2\2\2\u00e5\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9")
        buf.write("\3\2\2\2\2\u00eb\3\2\2\2\2\u00ed\3\2\2\2\3\u00f9\3\2\2")
        buf.write("\2\5\u00fd\3\2\2\2\7\u0101\3\2\2\2\t\u0104\3\2\2\2\13")
        buf.write("\u0107\3\2\2\2\r\u0109\3\2\2\2\17\u010b\3\2\2\2\21\u010d")
        buf.write("\3\2\2\2\23\u010f\3\2\2\2\25\u0111\3\2\2\2\27\u0114\3")
        buf.write("\2\2\2\31\u0116\3\2\2\2\33\u0118\3\2\2\2\35\u011c\3\2")
        buf.write("\2\2\37\u011f\3\2\2\2!\u0122\3\2\2\2#\u0125\3\2\2\2%\u0128")
        buf.write("\3\2\2\2\'\u012b\3\2\2\2)\u012d\3\2\2\2+\u0130\3\2\2\2")
        buf.write("-\u0132\3\2\2\2/\u0135\3\2\2\2\61\u0137\3\2\2\2\63\u013b")
        buf.write("\3\2\2\2\65\u013f\3\2\2\2\67\u0143\3\2\2\29\u014b\3\2")
        buf.write("\2\2;\u0156\3\2\2\2=\u015d\3\2\2\2?\u0166\3\2\2\2A\u0172")
        buf.write("\3\2\2\2C\u0176\3\2\2\2E\u017a\3\2\2\2G\u017f\3\2\2\2")
        buf.write("I\u0184\3\2\2\2K\u0188\3\2\2\2M\u018c\3\2\2\2O\u0191\3")
        buf.write("\2\2\2Q\u0195\3\2\2\2S\u0199\3\2\2\2U\u019c\3\2\2\2W\u019f")
        buf.write("\3\2\2\2Y\u01a2\3\2\2\2[\u01a5\3\2\2\2]\u01a8\3\2\2\2")
        buf.write("_\u01ab\3\2\2\2a\u01ae\3\2\2\2c\u01b2\3\2\2\2e\u01b5\3")
        buf.write("\2\2\2g\u01ba\3\2\2\2i\u01be\3\2\2\2k\u01c3\3\2\2\2m\u01d6")
        buf.write("\3\2\2\2o\u01ea\3\2\2\2q\u01ec\3\2\2\2s\u01ee\3\2\2\2")
        buf.write("u\u01f1\3\2\2\2w\u01f4\3\2\2\2y\u01f6\3\2\2\2{\u01f8\3")
        buf.write("\2\2\2}\u01fb\3\2\2\2\177\u01fd\3\2\2\2\u0081\u0204\3")
        buf.write("\2\2\2\u0083\u020a\3\2\2\2\u0085\u020f\3\2\2\2\u0087\u0212")
        buf.write("\3\2\2\2\u0089\u0217\3\2\2\2\u008b\u0223\3\2\2\2\u008d")
        buf.write("\u0226\3\2\2\2\u008f\u022b\3\2\2\2\u0091\u0232\3\2\2\2")
        buf.write("\u0093\u0234\3\2\2\2\u0095\u0238\3\2\2\2\u0097\u023a\3")
        buf.write("\2\2\2\u0099\u0240\3\2\2\2\u009b\u0246\3\2\2\2\u009d\u024d")
        buf.write("\3\2\2\2\u009f\u0251\3\2\2\2\u00a1\u0256\3\2\2\2\u00a3")
        buf.write("\u025f\3\2\2\2\u00a5\u0264\3\2\2\2\u00a7\u0268\3\2\2\2")
        buf.write("\u00a9\u026e\3\2\2\2\u00ab\u0278\3\2\2\2\u00ad\u027b\3")
        buf.write("\2\2\2\u00af\u0286\3\2\2\2\u00b1\u028d\3\2\2\2\u00b3\u0292")
        buf.write("\3\2\2\2\u00b5\u0296\3\2\2\2\u00b7\u0299\3\2\2\2\u00b9")
        buf.write("\u029e\3\2\2\2\u00bb\u02a3\3\2\2\2\u00bd\u02a5\3\2\2\2")
        buf.write("\u00bf\u02ab\3\2\2\2\u00c1\u02af\3\2\2\2\u00c3\u02b6\3")
        buf.write("\2\2\2\u00c5\u02bc\3\2\2\2\u00c7\u02be\3\2\2\2\u00c9\u02c2")
        buf.write("\3\2\2\2\u00cb\u02c5\3\2\2\2\u00cd\u02c7\3\2\2\2\u00cf")
        buf.write("\u02cc\3\2\2\2\u00d1\u02e0\3\2\2\2\u00d3\u02e2\3\2\2\2")
        buf.write("\u00d5\u02f2\3\2\2\2\u00d7\u02f4\3\2\2\2\u00d9\u02fb\3")
        buf.write("\2\2\2\u00db\u0300\3\2\2\2\u00dd\u0308\3\2\2\2\u00df\u030a")
        buf.write("\3\2\2\2\u00e1\u030d\3\2\2\2\u00e3\u0310\3\2\2\2\u00e5")
        buf.write("\u0313\3\2\2\2\u00e7\u0316\3\2\2\2\u00e9\u0319\3\2\2\2")
        buf.write("\u00eb\u031c\3\2\2\2\u00ed\u0320\3\2\2\2\u00ef\u0334\3")
        buf.write("\2\2\2\u00f1\u0350\3\2\2\2\u00f3\u0354\3\2\2\2\u00f5\u0356")
        buf.write("\3\2\2\2\u00f7\u035c\3\2\2\2\u00f9\u00fa\7\60\2\2\u00fa")
        buf.write("\u00fb\7\60\2\2\u00fb\u00fc\7\60\2\2\u00fc\4\3\2\2\2\u00fd")
        buf.write("\u00fe\7c\2\2\u00fe\u00ff\7p\2\2\u00ff\u0100\7f\2\2\u0100")
        buf.write("\6\3\2\2\2\u0101\u0102\7q\2\2\u0102\u0103\7t\2\2\u0103")
        buf.write("\b\3\2\2\2\u0104\u0105\7?\2\2\u0105\u0106\7@\2\2\u0106")
        buf.write("\n\3\2\2\2\u0107\u0108\7(\2\2\u0108\f\3\2\2\2\u0109\u010a")
        buf.write("\7~\2\2\u010a\16\3\2\2\2\u010b\u010c\7`\2\2\u010c\20\3")
        buf.write("\2\2\2\u010d\u010e\7/\2\2\u010e\22\3\2\2\2\u010f\u0110")
        buf.write("\7-\2\2\u0110\24\3\2\2\2\u0111\u0112\7\61\2\2\u0112\u0113")
        buf.write("\7\61\2\2\u0113\26\3\2\2\2\u0114\u0115\7\61\2\2\u0115")
        buf.write("\30\3\2\2\2\u0116\u0117\7\'\2\2\u0117\32\3\2\2\2\u0118")
        buf.write("\u0119\7o\2\2\u0119\u011a\7q\2\2\u011a\u011b\7f\2\2\u011b")
        buf.write("\34\3\2\2\2\u011c\u011d\7,\2\2\u011d\u011e\7,\2\2\u011e")
        buf.write("\36\3\2\2\2\u011f\u0120\7>\2\2\u0120\u0121\7>\2\2\u0121")
        buf.write(" \3\2\2\2\u0122\u0123\7@\2\2\u0123\u0124\7@\2\2\u0124")
        buf.write("\"\3\2\2\2\u0125\u0126\7?\2\2\u0126\u0127\7?\2\2\u0127")
        buf.write("$\3\2\2\2\u0128\u0129\7#\2\2\u0129\u012a\7?\2\2\u012a")
        buf.write("&\3\2\2\2\u012b\u012c\7>\2\2\u012c(\3\2\2\2\u012d\u012e")
        buf.write("\7>\2\2\u012e\u012f\7?\2\2\u012f*\3\2\2\2\u0130\u0131")
        buf.write("\7@\2\2\u0131,\3\2\2\2\u0132\u0133\7@\2\2\u0133\u0134")
        buf.write("\7?\2\2\u0134.\3\2\2\2\u0135\u0136\7\u0080\2\2\u0136\60")
        buf.write("\3\2\2\2\u0137\u0138\7c\2\2\u0138\u0139\7d\2\2\u0139\u013a")
        buf.write("\7u\2\2\u013a\62\3\2\2\2\u013b\u013c\7c\2\2\u013c\u013d")
        buf.write("\7n\2\2\u013d\u013e\7n\2\2\u013e\64\3\2\2\2\u013f\u0140")
        buf.write("\7c\2\2\u0140\u0141\7p\2\2\u0141\u0142\7{\2\2\u0142\66")
        buf.write("\3\2\2\2\u0143\u0144\7c\2\2\u0144\u0145\7v\2\2\u0145\u0146")
        buf.write("\7N\2\2\u0146\u0147\7c\2\2\u0147\u0148\7d\2\2\u0148\u0149")
        buf.write("\7g\2\2\u0149\u014a\7n\2\2\u014a8\3\2\2\2\u014b\u014c")
        buf.write("\7e\2\2\u014c\u014d\7q\2\2\u014d\u014e\7w\2\2\u014e\u014f")
        buf.write("\7p\2\2\u014f\u0150\7v\2\2\u0150\u0151\7N\2\2\u0151\u0152")
        buf.write("\7c\2\2\u0152\u0153\7d\2\2\u0153\u0154\7g\2\2\u0154\u0155")
        buf.write("\7n\2\2\u0155:\3\2\2\2\u0156\u0157\7e\2\2\u0157\u0158")
        buf.write("\7j\2\2\u0158\u0159\7q\2\2\u0159\u015a\7q\2\2\u015a\u015b")
        buf.write("\7u\2\2\u015b\u015c\7g\2\2\u015c<\3\2\2\2\u015d\u015e")
        buf.write("\7e\2\2\u015e\u015f\7q\2\2\u015f\u0160\7p\2\2\u0160\u0161")
        buf.write("\7v\2\2\u0161\u0162\7g\2\2\u0162\u0163\7z\2\2\u0163\u0164")
        buf.write("\7v\2\2\u0164\u0165\7u\2\2\u0165>\3\2\2\2\u0166\u0167")
        buf.write("\7i\2\2\u0167\u0168\7g\2\2\u0168\u0169\7v\2\2\u0169\u016a")
        buf.write("\7a\2\2\u016a\u016b\7e\2\2\u016b\u016c\7q\2\2\u016c\u016d")
        buf.write("\7p\2\2\u016d\u016e\7v\2\2\u016e\u016f\7g\2\2\u016f\u0170")
        buf.write("\7z\2\2\u0170\u0171\7v\2\2\u0171@\3\2\2\2\u0172\u0173")
        buf.write("\7o\2\2\u0173\u0174\7k\2\2\u0174\u0175\7p\2\2\u0175B\3")
        buf.write("\2\2\2\u0176\u0177\7o\2\2\u0177\u0178\7c\2\2\u0178\u0179")
        buf.write("\7z\2\2\u0179D\3\2\2\2\u017a\u017b\7m\2\2\u017b\u017c")
        buf.write("\7g\2\2\u017c\u017d\7{\2\2\u017d\u017e\7u\2\2\u017eF\3")
        buf.write("\2\2\2\u017f\u0180\7j\2\2\u0180\u0181\7c\2\2\u0181\u0182")
        buf.write("\7u\2\2\u0182\u0183\7j\2\2\u0183H\3\2\2\2\u0184\u0185")
        buf.write("\7n\2\2\u0185\u0186\7g\2\2\u0186\u0187\7p\2\2\u0187J\3")
        buf.write("\2\2\2\u0188\u0189\7g\2\2\u0189\u018a\7p\2\2\u018a\u018b")
        buf.write("\7f\2\2\u018bL\3\2\2\2\u018c\u018d\7c\2\2\u018d\u018e")
        buf.write("\7p\2\2\u018e\u018f\7f\2\2\u018f\u0190\7?\2\2\u0190N\3")
        buf.write("\2\2\2\u0191\u0192\7q\2\2\u0192\u0193\7t\2\2\u0193\u0194")
        buf.write("\7?\2\2\u0194P\3\2\2\2\u0195\u0196\7?\2\2\u0196\u0197")
        buf.write("\7@\2\2\u0197\u0198\7?\2\2\u0198R\3\2\2\2\u0199\u019a")
        buf.write("\7(\2\2\u019a\u019b\7?\2\2\u019bT\3\2\2\2\u019c\u019d")
        buf.write("\7~\2\2\u019d\u019e\7?\2\2\u019eV\3\2\2\2\u019f\u01a0")
        buf.write("\7`\2\2\u01a0\u01a1\7?\2\2\u01a1X\3\2\2\2\u01a2\u01a3")
        buf.write("\7/\2\2\u01a3\u01a4\7?\2\2\u01a4Z\3\2\2\2\u01a5\u01a6")
        buf.write("\7-\2\2\u01a6\u01a7\7?\2\2\u01a7\\\3\2\2\2\u01a8\u01a9")
        buf.write("\7,\2\2\u01a9\u01aa\7?\2\2\u01aa^\3\2\2\2\u01ab\u01ac")
        buf.write("\7\61\2\2\u01ac\u01ad\7?\2\2\u01ad`\3\2\2\2\u01ae\u01af")
        buf.write("\7\61\2\2\u01af\u01b0\7\61\2\2\u01b0\u01b1\7?\2\2\u01b1")
        buf.write("b\3\2\2\2\u01b2\u01b3\7\'\2\2\u01b3\u01b4\7?\2\2\u01b4")
        buf.write("d\3\2\2\2\u01b5\u01b6\7o\2\2\u01b6\u01b7\7q\2\2\u01b7")
        buf.write("\u01b8\7f\2\2\u01b8\u01b9\7?\2\2\u01b9f\3\2\2\2\u01ba")
        buf.write("\u01bb\7,\2\2\u01bb\u01bc\7,\2\2\u01bc\u01bd\7?\2\2\u01bd")
        buf.write("h\3\2\2\2\u01be\u01bf\7@\2\2\u01bf\u01c0\7@\2\2\u01c0")
        buf.write("\u01c1\7?\2\2\u01c1j\3\2\2\2\u01c2\u01c4\7\17\2\2\u01c3")
        buf.write("\u01c2\3\2\2\2\u01c3\u01c4\3\2\2\2\u01c4\u01c5\3\2\2\2")
        buf.write("\u01c5\u01c9\7\f\2\2\u01c6\u01c8\7\"\2\2\u01c7\u01c6\3")
        buf.write("\2\2\2\u01c8\u01cb\3\2\2\2\u01c9\u01c7\3\2\2\2\u01c9\u01ca")
        buf.write("\3\2\2\2\u01ca\u01cc\3\2\2\2\u01cb\u01c9\3\2\2\2\u01cc")
        buf.write("\u01cd\b\66\2\2\u01cdl\3\2\2\2\u01ce\u01d0\7\"\2\2\u01cf")
        buf.write("\u01ce\3\2\2\2\u01d0\u01d1\3\2\2\2\u01d1\u01cf\3\2\2\2")
        buf.write("\u01d1\u01d2\3\2\2\2\u01d2\u01d7\3\2\2\2\u01d3\u01d4\7")
        buf.write("^\2\2\u01d4\u01d7\5k\66\2\u01d5\u01d7\5o8\2\u01d6\u01cf")
        buf.write("\3\2\2\2\u01d6\u01d3\3\2\2\2\u01d6\u01d5\3\2\2\2\u01d7")
        buf.write("\u01d8\3\2\2\2\u01d8\u01d9\b\67\3\2\u01d9n\3\2\2\2\u01da")
        buf.write("\u01de\5s:\2\u01db\u01dd\13\2\2\2\u01dc\u01db\3\2\2\2")
        buf.write("\u01dd\u01e0\3\2\2\2\u01de\u01df\3\2\2\2\u01de\u01dc\3")
        buf.write("\2\2\2\u01df\u01e1\3\2\2\2\u01e0\u01de\3\2\2\2\u01e1\u01e2")
        buf.write("\5u;\2\u01e2\u01eb\3\2\2\2\u01e3\u01e7\5q9\2\u01e4\u01e6")
        buf.write("\n\2\2\2\u01e5\u01e4\3\2\2\2\u01e6\u01e9\3\2\2\2\u01e7")
        buf.write("\u01e5\3\2\2\2\u01e7\u01e8\3\2\2\2\u01e8\u01eb\3\2\2\2")
        buf.write("\u01e9\u01e7\3\2\2\2\u01ea\u01da\3\2\2\2\u01ea\u01e3\3")
        buf.write("\2\2\2\u01ebp\3\2\2\2\u01ec\u01ed\7%\2\2\u01edr\3\2\2")
        buf.write("\2\u01ee\u01ef\7*\2\2\u01ef\u01f0\7,\2\2\u01f0t\3\2\2")
        buf.write("\2\u01f1\u01f2\7,\2\2\u01f2\u01f3\7+\2\2\u01f3v\3\2\2")
        buf.write("\2\u01f4\u01f5\7#\2\2\u01f5x\3\2\2\2\u01f6\u01f7\7,\2")
        buf.write("\2\u01f7z\3\2\2\2\u01f8\u01f9\7c\2\2\u01f9\u01fa\7u\2")
        buf.write("\2\u01fa|\3\2\2\2\u01fb\u01fc\7\60\2\2\u01fc~\3\2\2\2")
        buf.write("\u01fd\u01fe\7k\2\2\u01fe\u01ff\7o\2\2\u01ff\u0200\7r")
        buf.write("\2\2\u0200\u0201\7q\2\2\u0201\u0202\7t\2\2\u0202\u0203")
        buf.write("\7v\2\2\u0203\u0080\3\2\2\2\u0204\u0205\7r\2\2\u0205\u0206")
        buf.write("\7t\2\2\u0206\u0207\7k\2\2\u0207\u0208\7p\2\2\u0208\u0209")
        buf.write("\7v\2\2\u0209\u0082\3\2\2\2\u020a\u020b\7h\2\2\u020b\u020c")
        buf.write("\7t\2\2\u020c\u020d\7q\2\2\u020d\u020e\7o\2\2\u020e\u0084")
        buf.write("\3\2\2\2\u020f\u0210\7\60\2\2\u0210\u0211\7\60\2\2\u0211")
        buf.write("\u0086\3\2\2\2\u0212\u0213\7f\2\2\u0213\u0214\7k\2\2\u0214")
        buf.write("\u0215\7e\2\2\u0215\u0216\7v\2\2\u0216\u0088\3\2\2\2\u0217")
        buf.write("\u0218\7u\2\2\u0218\u0219\7g\2\2\u0219\u021a\7v\2\2\u021a")
        buf.write("\u021b\7k\2\2\u021b\u021c\7p\2\2\u021c\u021d\7v\2\2\u021d")
        buf.write("\u021e\7n\2\2\u021e\u021f\7g\2\2\u021f\u0220\7x\2\2\u0220")
        buf.write("\u0221\7g\2\2\u0221\u0222\7n\2\2\u0222\u008a\3\2\2\2\u0223")
        buf.write("\u0224\7/\2\2\u0224\u0225\7@\2\2\u0225\u008c\3\2\2\2\u0226")
        buf.write("\u0227\7u\2\2\u0227\u0228\7v\2\2\u0228\u0229\7q\2\2\u0229")
        buf.write("\u022a\7r\2\2\u022a\u008e\3\2\2\2\u022b\u022c\7n\2\2\u022c")
        buf.write("\u022d\7c\2\2\u022d\u022e\7o\2\2\u022e\u022f\7d\2\2\u022f")
        buf.write("\u0230\7f\2\2\u0230\u0231\7c\2\2\u0231\u0090\3\2\2\2\u0232")
        buf.write("\u0233\7A\2\2\u0233\u0092\3\2\2\2\u0234\u0235\7p\2\2\u0235")
        buf.write("\u0236\7q\2\2\u0236\u0237\7v\2\2\u0237\u0094\3\2\2\2\u0238")
        buf.write("\u0239\7.\2\2\u0239\u0096\3\2\2\2\u023a\u023b\7e\2\2\u023b")
        buf.write("\u023c\7q\2\2\u023c\u023d\7p\2\2\u023d\u023e\7u\2\2\u023e")
        buf.write("\u023f\7v\2\2\u023f\u0098\3\2\2\2\u0240\u0241\7c\2\2\u0241")
        buf.write("\u0242\7y\2\2\u0242\u0243\7c\2\2\u0243\u0244\7k\2\2\u0244")
        buf.write("\u0245\7v\2\2\u0245\u009a\3\2\2\2\u0246\u0247\7c\2\2\u0247")
        buf.write("\u0248\7u\2\2\u0248\u0249\7u\2\2\u0249\u024a\7g\2\2\u024a")
        buf.write("\u024b\7t\2\2\u024b\u024c\7v\2\2\u024c\u009c\3\2\2\2\u024d")
        buf.write("\u024e\7x\2\2\u024e\u024f\7c\2\2\u024f\u0250\7t\2\2\u0250")
        buf.write("\u009e\3\2\2\2\u0251\u0252\7v\2\2\u0252\u0253\7t\2\2\u0253")
        buf.write("\u0254\7c\2\2\u0254\u0255\7r\2\2\u0255\u00a0\3\2\2\2\u0256")
        buf.write("\u0257\7r\2\2\u0257\u0258\7q\2\2\u0258\u0259\7u\2\2\u0259")
        buf.write("\u025a\7u\2\2\u025a\u025b\7k\2\2\u025b\u025c\7d\2\2\u025c")
        buf.write("\u025d\7n\2\2\u025d\u025e\7{\2\2\u025e\u00a2\3\2\2\2\u025f")
        buf.write("\u0260\7r\2\2\u0260\u0261\7c\2\2\u0261\u0262\7u\2\2\u0262")
        buf.write("\u0263\7u\2\2\u0263\u00a4\3\2\2\2\u0264\u0265\7f\2\2\u0265")
        buf.write("\u0266\7g\2\2\u0266\u0267\7n\2\2\u0267\u00a6\3\2\2\2\u0268")
        buf.write("\u0269\7u\2\2\u0269\u026a\7r\2\2\u026a\u026b\7c\2\2\u026b")
        buf.write("\u026c\7y\2\2\u026c\u026d\7p\2\2\u026d\u00a8\3\2\2\2\u026e")
        buf.write("\u026f\7k\2\2\u026f\u0270\7p\2\2\u0270\u0271\7x\2\2\u0271")
        buf.write("\u0272\7c\2\2\u0272\u0273\7t\2\2\u0273\u0274\7k\2\2\u0274")
        buf.write("\u0275\7c\2\2\u0275\u0276\7p\2\2\u0276\u0277\7v\2\2\u0277")
        buf.write("\u00aa\3\2\2\2\u0278\u0279\7i\2\2\u0279\u027a\7q\2\2\u027a")
        buf.write("\u00ac\3\2\2\2\u027b\u027c\7u\2\2\u027c\u027d\7g\2\2\u027d")
        buf.write("\u027e\7s\2\2\u027e\u027f\7w\2\2\u027f\u0280\7g\2\2\u0280")
        buf.write("\u0281\7p\2\2\u0281\u0282\7v\2\2\u0282\u0283\7k\2\2\u0283")
        buf.write("\u0284\7c\2\2\u0284\u0285\7n\2\2\u0285\u00ae\3\2\2\2\u0286")
        buf.write("\u0287\7c\2\2\u0287\u0288\7v\2\2\u0288\u0289\7q\2\2\u0289")
        buf.write("\u028a\7o\2\2\u028a\u028b\7k\2\2\u028b\u028c\7e\2\2\u028c")
        buf.write("\u00b0\3\2\2\2\u028d\u028e\7y\2\2\u028e\u028f\7j\2\2\u028f")
        buf.write("\u0290\7g\2\2\u0290\u0291\7p\2\2\u0291\u00b2\3\2\2\2\u0292")
        buf.write("\u0293\7n\2\2\u0293\u0294\7g\2\2\u0294\u0295\7v\2\2\u0295")
        buf.write("\u00b4\3\2\2\2\u0296\u0297\7k\2\2\u0297\u0298\7h\2\2\u0298")
        buf.write("\u00b6\3\2\2\2\u0299\u029a\7g\2\2\u029a\u029b\7n\2\2\u029b")
        buf.write("\u029c\7k\2\2\u029c\u029d\7h\2\2\u029d\u00b8\3\2\2\2\u029e")
        buf.write("\u029f\7g\2\2\u029f\u02a0\7n\2\2\u02a0\u02a1\7u\2\2\u02a1")
        buf.write("\u02a2\7g\2\2\u02a2\u00ba\3\2\2\2\u02a3\u02a4\7B\2\2\u02a4")
        buf.write("\u00bc\3\2\2\2\u02a5\u02a6\7y\2\2\u02a6\u02a7\7j\2\2\u02a7")
        buf.write("\u02a8\7k\2\2\u02a8\u02a9\7n\2\2\u02a9\u02aa\7g\2\2\u02aa")
        buf.write("\u00be\3\2\2\2\u02ab\u02ac\7f\2\2\u02ac\u02ad\7g\2\2\u02ad")
        buf.write("\u02ae\7h\2\2\u02ae\u00c0\3\2\2\2\u02af\u02b0\7g\2\2\u02b0")
        buf.write("\u02b1\7z\2\2\u02b1\u02b2\7k\2\2\u02b2\u02b3\7u\2\2\u02b3")
        buf.write("\u02b4\7v\2\2\u02b4\u02b5\7u\2\2\u02b5\u00c2\3\2\2\2\u02b6")
        buf.write("\u02b7\7y\2\2\u02b7\u02b8\7j\2\2\u02b8\u02b9\7g\2\2\u02b9")
        buf.write("\u02ba\7t\2\2\u02ba\u02bb\7g\2\2\u02bb\u00c4\3\2\2\2\u02bc")
        buf.write("\u02bd\7?\2\2\u02bd\u00c6\3\2\2\2\u02be\u02bf\7h\2\2\u02bf")
        buf.write("\u02c0\7q\2\2\u02c0\u02c1\7t\2\2\u02c1\u00c8\3\2\2\2\u02c2")
        buf.write("\u02c3\7k\2\2\u02c3\u02c4\7p\2\2\u02c4\u00ca\3\2\2\2\u02c5")
        buf.write("\u02c6\7<\2\2\u02c6\u00cc\3\2\2\2\u02c7\u02c8\7P\2\2\u02c8")
        buf.write("\u02c9\7q\2\2\u02c9\u02ca\7p\2\2\u02ca\u02cb\7g\2\2\u02cb")
        buf.write("\u00ce\3\2\2\2\u02cc\u02cd\7c\2\2\u02cd\u02ce\7v\2\2\u02ce")
        buf.write("\u02cf\7q\2\2\u02cf\u02d0\7o\2\2\u02d0\u02d1\7k\2\2\u02d1")
        buf.write("\u02d2\7e\2\2\u02d2\u02d3\7c\2\2\u02d3\u02d4\7n\2\2\u02d4")
        buf.write("\u02d5\7n\2\2\u02d5\u02d6\7{\2\2\u02d6\u00d0\3\2\2\2\u02d7")
        buf.write("\u02d8\7H\2\2\u02d8\u02d9\7c\2\2\u02d9\u02da\7n\2\2\u02da")
        buf.write("\u02db\7u\2\2\u02db\u02e1\7g\2\2\u02dc\u02dd\7V\2\2\u02dd")
        buf.write("\u02de\7t\2\2\u02de\u02df\7w\2\2\u02df\u02e1\7g\2\2\u02e0")
        buf.write("\u02d7\3\2\2\2\u02e0\u02dc\3\2\2\2\u02e1\u00d2\3\2\2\2")
        buf.write("\u02e2\u02e3\7g\2\2\u02e3\u02e4\7v\2\2\u02e4\u02e5\7g")
        buf.write("\2\2\u02e5\u02e6\7t\2\2\u02e6\u02e7\7p\2\2\u02e7\u02e8")
        buf.write("\7c\2\2\u02e8\u02e9\7n\2\2\u02e9\u00d4\3\2\2\2\u02ea\u02ec")
        buf.write("\t\3\2\2\u02eb\u02ea\3\2\2\2\u02ec\u02ed\3\2\2\2\u02ed")
        buf.write("\u02eb\3\2\2\2\u02ed\u02ee\3\2\2\2\u02ee\u02f3\3\2\2\2")
        buf.write("\u02ef\u02f0\7k\2\2\u02f0\u02f1\7p\2\2\u02f1\u02f3\7h")
        buf.write("\2\2\u02f2\u02eb\3\2\2\2\u02f2\u02ef\3\2\2\2\u02f3\u00d6")
        buf.write("\3\2\2\2\u02f4\u02f8\t\4\2\2\u02f5\u02f7\t\5\2\2\u02f6")
        buf.write("\u02f5\3\2\2\2\u02f7\u02fa\3\2\2\2\u02f8\u02f6\3\2\2\2")
        buf.write("\u02f8\u02f9\3\2\2\2\u02f9\u00d8\3\2\2\2\u02fa\u02f8\3")
        buf.write("\2\2\2\u02fb\u02fe\t\6\2\2\u02fc\u02ff\5\u00dbn\2\u02fd")
        buf.write("\u02ff\5\u00d7l\2\u02fe\u02fc\3\2\2\2\u02fe\u02fd\3\2")
        buf.write("\2\2\u02ff\u00da\3\2\2\2\u0300\u0301\7\62\2\2\u0301\u0302")
        buf.write("\7Z\2\2\u0302\u0304\3\2\2\2\u0303\u0305\5\u00ddo\2\u0304")
        buf.write("\u0303\3\2\2\2\u0305\u0306\3\2\2\2\u0306\u0304\3\2\2\2")
        buf.write("\u0306\u0307\3\2\2\2\u0307\u00dc\3\2\2\2\u0308\u0309\t")
        buf.write("\7\2\2\u0309\u00de\3\2\2\2\u030a\u030b\7]\2\2\u030b\u030c")
        buf.write("\bp\4\2\u030c\u00e0\3\2\2\2\u030d\u030e\7_\2\2\u030e\u030f")
        buf.write("\bq\5\2\u030f\u00e2\3\2\2\2\u0310\u0311\7}\2\2\u0311\u0312")
        buf.write("\br\6\2\u0312\u00e4\3\2\2\2\u0313\u0314\7\177\2\2\u0314")
        buf.write("\u0315\bs\7\2\u0315\u00e6\3\2\2\2\u0316\u0317\7*\2\2\u0317")
        buf.write("\u0318\bt\b\2\u0318\u00e8\3\2\2\2\u0319\u031a\7+\2\2\u031a")
        buf.write("\u031b\bu\t\2\u031b\u00ea\3\2\2\2\u031c\u031d\7=\2\2\u031d")
        buf.write("\u00ec\3\2\2\2\u031e\u0321\5\u00efx\2\u031f\u0321\5\u00f1")
        buf.write("y\2\u0320\u031e\3\2\2\2\u0320\u031f\3\2\2\2\u0321\u00ee")
        buf.write("\3\2\2\2\u0322\u0327\7)\2\2\u0323\u0326\5\u00f7|\2\u0324")
        buf.write("\u0326\n\b\2\2\u0325\u0323\3\2\2\2\u0325\u0324\3\2\2\2")
        buf.write("\u0326\u0329\3\2\2\2\u0327\u0325\3\2\2\2\u0327\u0328\3")
        buf.write("\2\2\2\u0328\u032a\3\2\2\2\u0329\u0327\3\2\2\2\u032a\u0335")
        buf.write("\7)\2\2\u032b\u0330\7$\2\2\u032c\u032f\5\u00f7|\2\u032d")
        buf.write("\u032f\n\t\2\2\u032e\u032c\3\2\2\2\u032e\u032d\3\2\2\2")
        buf.write("\u032f\u0332\3\2\2\2\u0330\u032e\3\2\2\2\u0330\u0331\3")
        buf.write("\2\2\2\u0331\u0333\3\2\2\2\u0332\u0330\3\2\2\2\u0333\u0335")
        buf.write("\7$\2\2\u0334\u0322\3\2\2\2\u0334\u032b\3\2\2\2\u0335")
        buf.write("\u00f0\3\2\2\2\u0336\u0337\7)\2\2\u0337\u0338\7)\2\2\u0338")
        buf.write("\u0339\7)\2\2\u0339\u033d\3\2\2\2\u033a\u033c\5\u00f3")
        buf.write("z\2\u033b\u033a\3\2\2\2\u033c\u033f\3\2\2\2\u033d\u033e")
        buf.write("\3\2\2\2\u033d\u033b\3\2\2\2\u033e\u0340\3\2\2\2\u033f")
        buf.write("\u033d\3\2\2\2\u0340\u0341\7)\2\2\u0341\u0342\7)\2\2\u0342")
        buf.write("\u0351\7)\2\2\u0343\u0344\7$\2\2\u0344\u0345\7$\2\2\u0345")
        buf.write("\u0346\7$\2\2\u0346\u034a\3\2\2\2\u0347\u0349\5\u00f3")
        buf.write("z\2\u0348\u0347\3\2\2\2\u0349\u034c\3\2\2\2\u034a\u034b")
        buf.write("\3\2\2\2\u034a\u0348\3\2\2\2\u034b\u034d\3\2\2\2\u034c")
        buf.write("\u034a\3\2\2\2\u034d\u034e\7$\2\2\u034e\u034f\7$\2\2\u034f")
        buf.write("\u0351\7$\2\2\u0350\u0336\3\2\2\2\u0350\u0343\3\2\2\2")
        buf.write("\u0351\u00f2\3\2\2\2\u0352\u0355\5\u00f5{\2\u0353\u0355")
        buf.write("\5\u00f7|\2\u0354\u0352\3\2\2\2\u0354\u0353\3\2\2\2\u0355")
        buf.write("\u00f4\3\2\2\2\u0356\u0357\n\n\2\2\u0357\u00f6\3\2\2\2")
        buf.write("\u0358\u0359\7^\2\2\u0359\u035d\13\2\2\2\u035a\u035b\7")
        buf.write("^\2\2\u035b\u035d\5k\66\2\u035c\u0358\3\2\2\2\u035c\u035a")
        buf.write("\3\2\2\2\u035d\u00f8\3\2\2\2\33\2\u01c3\u01c9\u01d1\u01d6")
        buf.write("\u01de\u01e7\u01ea\u02e0\u02ed\u02f2\u02f8\u02fe\u0306")
        buf.write("\u0320\u0325\u0327\u032e\u0330\u0334\u033d\u034a\u0350")
        buf.write("\u0354\u035c\n\3\66\2\b\2\2\3p\3\3q\4\3r\5\3s\6\3t\7\3")
        buf.write("u\b")
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
    NL = 53
    WS = 54
    COMMENT_START = 55
    OPEN_MULTI_COMMENT = 56
    CLOSE_MULTI_COMMENT = 57
    POINTER_OF = 58
    STAR = 59
    AS = 60
    DOT = 61
    IMPORT = 62
    PRINT = 63
    FROM = 64
    RANGE = 65
    DICT = 66
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
    ATOMIC = 86
    WHEN = 87
    LET = 88
    IF = 89
    ELIF = 90
    ELSE = 91
    AT = 92
    WHILE = 93
    DEF = 94
    EXISTS = 95
    WHERE = 96
    EQ = 97
    FOR = 98
    IN = 99
    COLON = 100
    NONE = 101
    ATOMICALLY = 102
    BOOL = 103
    ETERNAL = 104
    INT = 105
    NAME = 106
    ATOM = 107
    HEX_INTEGER = 108
    OPEN_BRACK = 109
    CLOSE_BRACK = 110
    OPEN_BRACES = 111
    CLOSE_BRACES = 112
    OPEN_PAREN = 113
    CLOSE_PAREN = 114
    SEMI_COLON = 115
    STRING = 116

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'...'", "'and'", "'or'", "'=>'", "'&'", "'|'", "'^'", "'-'", 
            "'+'", "'//'", "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", 
            "'=='", "'!='", "'<'", "'<='", "'>'", "'>='", "'~'", "'abs'", 
            "'all'", "'any'", "'atLabel'", "'countLabel'", "'choose'", "'contexts'", 
            "'get_context'", "'min'", "'max'", "'keys'", "'hash'", "'len'", 
            "'end'", "'and='", "'or='", "'=>='", "'&='", "'|='", "'^='", 
            "'-='", "'+='", "'*='", "'/='", "'//='", "'%='", "'mod='", "'**='", 
            "'>>='", "'#'", "'(*'", "'*)'", "'!'", "'*'", "'as'", "'.'", 
            "'import'", "'print'", "'from'", "'..'", "'dict'", "'setintlevel'", 
            "'->'", "'stop'", "'lambda'", "'?'", "'not'", "','", "'const'", 
            "'await'", "'assert'", "'var'", "'trap'", "'possibly'", "'pass'", 
            "'del'", "'spawn'", "'invariant'", "'go'", "'sequential'", "'atomic'", 
            "'when'", "'let'", "'if'", "'elif'", "'else'", "'@'", "'while'", 
            "'def'", "'exists'", "'where'", "'='", "'for'", "'in'", "':'", 
            "'None'", "'atomically'", "'eternal'", "'['", "']'", "'{'", 
            "'}'", "'('", "')'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "NL", "WS", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
            "POINTER_OF", "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", 
            "RANGE", "DICT", "SETINTLEVEL", "ARROW", "STOP", "LAMBDA", "ADDRESS_OF", 
            "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", "VAR", "TRAP", "POSSIBLY", 
            "PASS", "DEL", "SPAWN", "INVARIANT", "GO", "SEQUENTIAL", "ATOMIC", 
            "WHEN", "LET", "IF", "ELIF", "ELSE", "AT", "WHILE", "DEF", "EXISTS", 
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
                  "T__50", "T__51", "NL", "WS", "COMMENT", "COMMENT_START", 
                  "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", "POINTER_OF", 
                  "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", "RANGE", 
                  "DICT", "SETINTLEVEL", "ARROW", "STOP", "LAMBDA", "ADDRESS_OF", 
                  "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", "VAR", "TRAP", 
                  "POSSIBLY", "PASS", "DEL", "SPAWN", "INVARIANT", "GO", 
                  "SEQUENTIAL", "ATOMIC", "WHEN", "LET", "IF", "ELIF", "ELSE", 
                  "AT", "WHILE", "DEF", "EXISTS", "WHERE", "EQ", "FOR", 
                  "IN", "COLON", "NONE", "ATOMICALLY", "BOOL", "ETERNAL", 
                  "INT", "NAME", "ATOM", "HEX_INTEGER", "HEX_DIGIT", "OPEN_BRACK", 
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
            actions[52] = self.NL_action 
            actions[110] = self.OPEN_BRACK_action 
            actions[111] = self.CLOSE_BRACK_action 
            actions[112] = self.OPEN_BRACES_action 
            actions[113] = self.CLOSE_BRACES_action 
            actions[114] = self.OPEN_PAREN_action 
            actions[115] = self.CLOSE_PAREN_action 
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
     


