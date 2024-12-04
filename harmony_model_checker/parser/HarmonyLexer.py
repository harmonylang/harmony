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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\u0081")
        buf.write("\u03da\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("y\ty\4z\tz\4{\t{\4|\t|\4}\t}\4~\t~\4\177\t\177\4\u0080")
        buf.write("\t\u0080\4\u0081\t\u0081\4\u0082\t\u0082\4\u0083\t\u0083")
        buf.write("\4\u0084\t\u0084\4\u0085\t\u0085\4\u0086\t\u0086\4\u0087")
        buf.write("\t\u0087\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3")
        buf.write("\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\13\3\13\3")
        buf.write("\f\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3")
        buf.write("\17\3\20\3\20\3\20\3\21\3\21\3\21\3\22\3\22\3\23\3\23")
        buf.write("\3\23\3\24\3\24\3\25\3\25\3\25\3\26\3\26\3\26\3\27\3\27")
        buf.write("\3\30\3\30\3\31\3\31\3\32\3\32\3\32\3\32\3\33\3\33\3\33")
        buf.write("\3\33\3\34\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\36\3\36")
        buf.write("\3\36\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3\37")
        buf.write("\3\37\3\37\3\37\3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3")
        buf.write("!\3!\3!\3!\3!\3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3\"\3#\3")
        buf.write("#\3#\3#\3$\3$\3$\3$\3%\3%\3%\3%\3%\3&\3&\3&\3&\3\'\3\'")
        buf.write("\3\'\3\'\3\'\3(\3(\3(\3(\3)\3)\3)\3)\3*\3*\3*\3*\3*\3")
        buf.write("*\3*\3*\3*\3+\3+\3+\3+\3,\3,\3,\3,\3,\3,\3,\3-\3-\3-\3")
        buf.write("-\3.\3.\3.\3.\3/\3/\3/\3/\3/\3\60\3\60\3\60\3\60\3\61")
        buf.write("\3\61\3\61\3\61\3\61\3\62\3\62\3\62\3\62\3\63\3\63\3\63")
        buf.write("\3\63\3\64\3\64\3\64\3\65\3\65\3\65\3\66\3\66\3\66\3\67")
        buf.write("\3\67\3\67\38\38\38\39\39\39\3:\3:\3:\3;\3;\3;\3;\3<\3")
        buf.write("<\3<\3=\3=\3=\3=\3=\3>\3>\3>\3>\3?\3?\3?\3?\3@\3@\3@\3")
        buf.write("@\3A\5A\u0207\nA\3A\3A\7A\u020b\nA\fA\16A\u020e\13A\3")
        buf.write("A\7A\u0211\nA\fA\16A\u0214\13A\5A\u0216\nA\3A\3A\3B\6")
        buf.write("B\u021b\nB\rB\16B\u021c\3B\6B\u0220\nB\rB\16B\u0221\3")
        buf.write("B\3B\3B\5B\u0227\nB\3B\3B\3C\3C\7C\u022d\nC\fC\16C\u0230")
        buf.write("\13C\3C\3C\3C\3C\7C\u0236\nC\fC\16C\u0239\13C\5C\u023b")
        buf.write("\nC\3D\3D\3E\3E\3E\3F\3F\3F\3G\3G\3H\3H\3H\3I\3I\3J\3")
        buf.write("J\3J\3J\3J\3J\3J\3K\3K\3K\3K\3K\3K\3L\3L\3L\3L\3L\3M\3")
        buf.write("M\3M\3N\3N\3N\3N\3N\3N\3N\3N\3N\3N\3N\3N\3O\3O\3O\3O\3")
        buf.write("O\3P\3P\3P\3P\3P\3Q\3Q\3Q\3Q\3Q\3Q\3Q\3R\3R\3R\3R\3S\3")
        buf.write("S\3T\3T\3T\3T\3T\3T\3U\3U\3U\3U\3U\3U\3V\3V\3V\3V\3V\3")
        buf.write("V\3V\3W\3W\3W\3W\3X\3X\3X\3X\3X\3Y\3Y\3Y\3Y\3Y\3Z\3Z\3")
        buf.write("Z\3Z\3[\3[\3[\3[\3[\3[\3\\\3\\\3\\\3\\\3\\\3\\\3\\\3\\")
        buf.write("\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3^\3^\3^\3_\3_\3_\3_\3")
        buf.write("_\3_\3_\3_\3`\3`\3`\3`\3`\3`\3`\3`\3`\3`\3`\3a\3a\3a\3")
        buf.write("a\3a\3b\3b\3b\3b\3c\3c\3c\3d\3d\3d\3d\3d\3e\3e\3e\3e\3")
        buf.write("e\3f\3f\3g\3g\3g\3g\3g\3g\3h\3h\3h\3h\3h\3h\3h\3i\3i\3")
        buf.write("i\3i\3j\3j\3j\3j\3j\3j\3j\3j\3k\3k\3k\3k\3k\3k\3k\3l\3")
        buf.write("l\3l\3l\3l\3l\3m\3m\3n\3n\3n\3n\3n\3n\3o\3o\3o\3o\3o\3")
        buf.write("p\3p\3q\3q\3q\3q\3q\3r\3r\3r\3r\3r\3r\3r\3r\3r\3r\3r\3")
        buf.write("s\3s\3s\3s\3s\3s\3s\3s\3s\5s\u033d\ns\3t\3t\3t\3t\3t\3")
        buf.write("t\3t\3t\3u\6u\u0348\nu\ru\16u\u0349\3u\3u\3u\3u\6u\u0350")
        buf.write("\nu\ru\16u\u0351\3u\3u\3u\3u\6u\u0358\nu\ru\16u\u0359")
        buf.write("\3u\3u\3u\3u\6u\u0360\nu\ru\16u\u0361\5u\u0364\nu\3v\3")
        buf.write("v\7v\u0368\nv\fv\16v\u036b\13v\3w\3w\3w\5w\u0370\nw\3")
        buf.write("x\3x\3x\3x\7x\u0376\nx\fx\16x\u0379\13x\3x\3x\3y\3y\3")
        buf.write("y\3y\6y\u0381\ny\ry\16y\u0382\3z\3z\3{\3{\3{\3|\3|\3|")
        buf.write("\3}\3}\3}\3~\3~\3~\3\177\3\177\3\177\3\u0080\3\u0080\3")
        buf.write("\u0080\3\u0081\3\u0081\3\u0082\3\u0082\5\u0082\u039d\n")
        buf.write("\u0082\3\u0083\3\u0083\3\u0083\7\u0083\u03a2\n\u0083\f")
        buf.write("\u0083\16\u0083\u03a5\13\u0083\3\u0083\3\u0083\3\u0083")
        buf.write("\3\u0083\7\u0083\u03ab\n\u0083\f\u0083\16\u0083\u03ae")
        buf.write("\13\u0083\3\u0083\5\u0083\u03b1\n\u0083\3\u0084\3\u0084")
        buf.write("\3\u0084\3\u0084\3\u0084\7\u0084\u03b8\n\u0084\f\u0084")
        buf.write("\16\u0084\u03bb\13\u0084\3\u0084\3\u0084\3\u0084\3\u0084")
        buf.write("\3\u0084\3\u0084\3\u0084\3\u0084\7\u0084\u03c5\n\u0084")
        buf.write("\f\u0084\16\u0084\u03c8\13\u0084\3\u0084\3\u0084\3\u0084")
        buf.write("\5\u0084\u03cd\n\u0084\3\u0085\3\u0085\5\u0085\u03d1\n")
        buf.write("\u0085\3\u0086\3\u0086\3\u0087\3\u0087\3\u0087\3\u0087")
        buf.write("\5\u0087\u03d9\n\u0087\5\u022e\u03b9\u03c6\2\u0088\3\3")
        buf.write("\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16")
        buf.write("\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61")
        buf.write("\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*")
        buf.write("S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q:s;u<w")
        buf.write("=y>{?}@\177A\u0081B\u0083C\u0085\2\u0087D\u0089E\u008b")
        buf.write("F\u008dG\u008fH\u0091I\u0093J\u0095K\u0097L\u0099M\u009b")
        buf.write("N\u009dO\u009fP\u00a1Q\u00a3R\u00a5S\u00a7T\u00a9U\u00ab")
        buf.write("V\u00adW\u00afX\u00b1Y\u00b3Z\u00b5[\u00b7\\\u00b9]\u00bb")
        buf.write("^\u00bd_\u00bf`\u00c1a\u00c3b\u00c5c\u00c7d\u00c9e\u00cb")
        buf.write("f\u00cdg\u00cfh\u00d1i\u00d3j\u00d5k\u00d7l\u00d9m\u00db")
        buf.write("n\u00ddo\u00dfp\u00e1q\u00e3r\u00e5s\u00e7t\u00e9u\u00eb")
        buf.write("v\u00edw\u00efx\u00f1y\u00f3\2\u00f5z\u00f7{\u00f9|\u00fb")
        buf.write("}\u00fd~\u00ff\177\u0101\u0080\u0103\u0081\u0105\2\u0107")
        buf.write("\2\u0109\2\u010b\2\u010d\2\3\2\r\4\2\f\f\16\17\3\2\62")
        buf.write(";\5\2\62;CHch\3\2\62\63\3\2\629\5\2C\\aac|\6\2\62;C\\")
        buf.write("aac|\3\2\60\60\6\2\f\f\16\17))^^\6\2\f\f\16\17$$^^\3\2")
        buf.write("^^\2\u03f5\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2")
        buf.write("\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2")
        buf.write("\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2")
        buf.write("\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#")
        buf.write("\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2")
        buf.write("\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65")
        buf.write("\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2")
        buf.write("\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2")
        buf.write("\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2")
        buf.write("\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3")
        buf.write("\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e")
        buf.write("\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2")
        buf.write("o\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2")
        buf.write("\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081")
        buf.write("\3\2\2\2\2\u0083\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2")
        buf.write("\2\2\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f\3\2\2\2\2\u0091")
        buf.write("\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2\2\2\u0097\3\2\2")
        buf.write("\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d\3\2\2\2\2\u009f")
        buf.write("\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2\2\2\u00a5\3\2\2")
        buf.write("\2\2\u00a7\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab\3\2\2\2\2\u00ad")
        buf.write("\3\2\2\2\2\u00af\3\2\2\2\2\u00b1\3\2\2\2\2\u00b3\3\2\2")
        buf.write("\2\2\u00b5\3\2\2\2\2\u00b7\3\2\2\2\2\u00b9\3\2\2\2\2\u00bb")
        buf.write("\3\2\2\2\2\u00bd\3\2\2\2\2\u00bf\3\2\2\2\2\u00c1\3\2\2")
        buf.write("\2\2\u00c3\3\2\2\2\2\u00c5\3\2\2\2\2\u00c7\3\2\2\2\2\u00c9")
        buf.write("\3\2\2\2\2\u00cb\3\2\2\2\2\u00cd\3\2\2\2\2\u00cf\3\2\2")
        buf.write("\2\2\u00d1\3\2\2\2\2\u00d3\3\2\2\2\2\u00d5\3\2\2\2\2\u00d7")
        buf.write("\3\2\2\2\2\u00d9\3\2\2\2\2\u00db\3\2\2\2\2\u00dd\3\2\2")
        buf.write("\2\2\u00df\3\2\2\2\2\u00e1\3\2\2\2\2\u00e3\3\2\2\2\2\u00e5")
        buf.write("\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9\3\2\2\2\2\u00eb\3\2\2")
        buf.write("\2\2\u00ed\3\2\2\2\2\u00ef\3\2\2\2\2\u00f1\3\2\2\2\2\u00f5")
        buf.write("\3\2\2\2\2\u00f7\3\2\2\2\2\u00f9\3\2\2\2\2\u00fb\3\2\2")
        buf.write("\2\2\u00fd\3\2\2\2\2\u00ff\3\2\2\2\2\u0101\3\2\2\2\2\u0103")
        buf.write("\3\2\2\2\3\u010f\3\2\2\2\5\u0113\3\2\2\2\7\u0116\3\2\2")
        buf.write("\2\t\u0118\3\2\2\2\13\u011a\3\2\2\2\r\u011c\3\2\2\2\17")
        buf.write("\u011e\3\2\2\2\21\u0120\3\2\2\2\23\u0123\3\2\2\2\25\u0125")
        buf.write("\3\2\2\2\27\u0127\3\2\2\2\31\u012b\3\2\2\2\33\u012e\3")
        buf.write("\2\2\2\35\u0131\3\2\2\2\37\u0134\3\2\2\2!\u0137\3\2\2")
        buf.write("\2#\u013a\3\2\2\2%\u013c\3\2\2\2\'\u013f\3\2\2\2)\u0141")
        buf.write("\3\2\2\2+\u0144\3\2\2\2-\u0147\3\2\2\2/\u0149\3\2\2\2")
        buf.write("\61\u014b\3\2\2\2\63\u014d\3\2\2\2\65\u0151\3\2\2\2\67")
        buf.write("\u0155\3\2\2\29\u0159\3\2\2\2;\u015d\3\2\2\2=\u0164\3")
        buf.write("\2\2\2?\u016d\3\2\2\2A\u0179\3\2\2\2C\u0183\3\2\2\2E\u0188")
        buf.write("\3\2\2\2G\u018c\3\2\2\2I\u0190\3\2\2\2K\u0195\3\2\2\2")
        buf.write("M\u0199\3\2\2\2O\u019e\3\2\2\2Q\u01a2\3\2\2\2S\u01a6\3")
        buf.write("\2\2\2U\u01af\3\2\2\2W\u01b3\3\2\2\2Y\u01ba\3\2\2\2[\u01be")
        buf.write("\3\2\2\2]\u01c2\3\2\2\2_\u01c7\3\2\2\2a\u01cb\3\2\2\2")
        buf.write("c\u01d0\3\2\2\2e\u01d4\3\2\2\2g\u01d8\3\2\2\2i\u01db\3")
        buf.write("\2\2\2k\u01de\3\2\2\2m\u01e1\3\2\2\2o\u01e4\3\2\2\2q\u01e7")
        buf.write("\3\2\2\2s\u01ea\3\2\2\2u\u01ed\3\2\2\2w\u01f1\3\2\2\2")
        buf.write("y\u01f4\3\2\2\2{\u01f9\3\2\2\2}\u01fd\3\2\2\2\177\u0201")
        buf.write("\3\2\2\2\u0081\u0206\3\2\2\2\u0083\u0226\3\2\2\2\u0085")
        buf.write("\u023a\3\2\2\2\u0087\u023c\3\2\2\2\u0089\u023e\3\2\2\2")
        buf.write("\u008b\u0241\3\2\2\2\u008d\u0244\3\2\2\2\u008f\u0246\3")
        buf.write("\2\2\2\u0091\u0249\3\2\2\2\u0093\u024b\3\2\2\2\u0095\u0252")
        buf.write("\3\2\2\2\u0097\u0258\3\2\2\2\u0099\u025d\3\2\2\2\u009b")
        buf.write("\u0260\3\2\2\2\u009d\u026c\3\2\2\2\u009f\u0271\3\2\2\2")
        buf.write("\u00a1\u0276\3\2\2\2\u00a3\u027d\3\2\2\2\u00a5\u0281\3")
        buf.write("\2\2\2\u00a7\u0283\3\2\2\2\u00a9\u0289\3\2\2\2\u00ab\u028f")
        buf.write("\3\2\2\2\u00ad\u0296\3\2\2\2\u00af\u029a\3\2\2\2\u00b1")
        buf.write("\u029f\3\2\2\2\u00b3\u02a4\3\2\2\2\u00b5\u02a8\3\2\2\2")
        buf.write("\u00b7\u02ae\3\2\2\2\u00b9\u02b6\3\2\2\2\u00bb\u02c0\3")
        buf.write("\2\2\2\u00bd\u02c3\3\2\2\2\u00bf\u02cb\3\2\2\2\u00c1\u02d6")
        buf.write("\3\2\2\2\u00c3\u02db\3\2\2\2\u00c5\u02df\3\2\2\2\u00c7")
        buf.write("\u02e2\3\2\2\2\u00c9\u02e7\3\2\2\2\u00cb\u02ec\3\2\2\2")
        buf.write("\u00cd\u02ee\3\2\2\2\u00cf\u02f4\3\2\2\2\u00d1\u02fb\3")
        buf.write("\2\2\2\u00d3\u02ff\3\2\2\2\u00d5\u0307\3\2\2\2\u00d7\u030e")
        buf.write("\3\2\2\2\u00d9\u0314\3\2\2\2\u00db\u0316\3\2\2\2\u00dd")
        buf.write("\u031c\3\2\2\2\u00df\u0321\3\2\2\2\u00e1\u0323\3\2\2\2")
        buf.write("\u00e3\u0328\3\2\2\2\u00e5\u033c\3\2\2\2\u00e7\u033e\3")
        buf.write("\2\2\2\u00e9\u0363\3\2\2\2\u00eb\u0365\3\2\2\2\u00ed\u036c")
        buf.write("\3\2\2\2\u00ef\u0371\3\2\2\2\u00f1\u037c\3\2\2\2\u00f3")
        buf.write("\u0384\3\2\2\2\u00f5\u0386\3\2\2\2\u00f7\u0389\3\2\2\2")
        buf.write("\u00f9\u038c\3\2\2\2\u00fb\u038f\3\2\2\2\u00fd\u0392\3")
        buf.write("\2\2\2\u00ff\u0395\3\2\2\2\u0101\u0398\3\2\2\2\u0103\u039c")
        buf.write("\3\2\2\2\u0105\u03b0\3\2\2\2\u0107\u03cc\3\2\2\2\u0109")
        buf.write("\u03d0\3\2\2\2\u010b\u03d2\3\2\2\2\u010d\u03d8\3\2\2\2")
        buf.write("\u010f\u0110\7c\2\2\u0110\u0111\7p\2\2\u0111\u0112\7f")
        buf.write("\2\2\u0112\4\3\2\2\2\u0113\u0114\7q\2\2\u0114\u0115\7")
        buf.write("t\2\2\u0115\6\3\2\2\2\u0116\u0117\7(\2\2\u0117\b\3\2\2")
        buf.write("\2\u0118\u0119\7~\2\2\u0119\n\3\2\2\2\u011a\u011b\7`\2")
        buf.write("\2\u011b\f\3\2\2\2\u011c\u011d\7/\2\2\u011d\16\3\2\2\2")
        buf.write("\u011e\u011f\7-\2\2\u011f\20\3\2\2\2\u0120\u0121\7\61")
        buf.write("\2\2\u0121\u0122\7\61\2\2\u0122\22\3\2\2\2\u0123\u0124")
        buf.write("\7\61\2\2\u0124\24\3\2\2\2\u0125\u0126\7\'\2\2\u0126\26")
        buf.write("\3\2\2\2\u0127\u0128\7o\2\2\u0128\u0129\7q\2\2\u0129\u012a")
        buf.write("\7f\2\2\u012a\30\3\2\2\2\u012b\u012c\7,\2\2\u012c\u012d")
        buf.write("\7,\2\2\u012d\32\3\2\2\2\u012e\u012f\7>\2\2\u012f\u0130")
        buf.write("\7>\2\2\u0130\34\3\2\2\2\u0131\u0132\7@\2\2\u0132\u0133")
        buf.write("\7@\2\2\u0133\36\3\2\2\2\u0134\u0135\7?\2\2\u0135\u0136")
        buf.write("\7?\2\2\u0136 \3\2\2\2\u0137\u0138\7#\2\2\u0138\u0139")
        buf.write("\7?\2\2\u0139\"\3\2\2\2\u013a\u013b\7>\2\2\u013b$\3\2")
        buf.write("\2\2\u013c\u013d\7>\2\2\u013d\u013e\7?\2\2\u013e&\3\2")
        buf.write("\2\2\u013f\u0140\7@\2\2\u0140(\3\2\2\2\u0141\u0142\7@")
        buf.write("\2\2\u0142\u0143\7?\2\2\u0143*\3\2\2\2\u0144\u0145\7?")
        buf.write("\2\2\u0145\u0146\7@\2\2\u0146,\3\2\2\2\u0147\u0148\7\u0080")
        buf.write("\2\2\u0148.\3\2\2\2\u0149\u014a\7A\2\2\u014a\60\3\2\2")
        buf.write("\2\u014b\u014c\7#\2\2\u014c\62\3\2\2\2\u014d\u014e\7c")
        buf.write("\2\2\u014e\u014f\7d\2\2\u014f\u0150\7u\2\2\u0150\64\3")
        buf.write("\2\2\2\u0151\u0152\7c\2\2\u0152\u0153\7n\2\2\u0153\u0154")
        buf.write("\7n\2\2\u0154\66\3\2\2\2\u0155\u0156\7c\2\2\u0156\u0157")
        buf.write("\7p\2\2\u0157\u0158\7{\2\2\u01588\3\2\2\2\u0159\u015a")
        buf.write("\7d\2\2\u015a\u015b\7k\2\2\u015b\u015c\7p\2\2\u015c:\3")
        buf.write("\2\2\2\u015d\u015e\7e\2\2\u015e\u015f\7j\2\2\u015f\u0160")
        buf.write("\7q\2\2\u0160\u0161\7q\2\2\u0161\u0162\7u\2\2\u0162\u0163")
        buf.write("\7g\2\2\u0163<\3\2\2\2\u0164\u0165\7e\2\2\u0165\u0166")
        buf.write("\7q\2\2\u0166\u0167\7p\2\2\u0167\u0168\7v\2\2\u0168\u0169")
        buf.write("\7g\2\2\u0169\u016a\7z\2\2\u016a\u016b\7v\2\2\u016b\u016c")
        buf.write("\7u\2\2\u016c>\3\2\2\2\u016d\u016e\7i\2\2\u016e\u016f")
        buf.write("\7g\2\2\u016f\u0170\7v\2\2\u0170\u0171\7a\2\2\u0171\u0172")
        buf.write("\7e\2\2\u0172\u0173\7q\2\2\u0173\u0174\7p\2\2\u0174\u0175")
        buf.write("\7v\2\2\u0175\u0176\7g\2\2\u0176\u0177\7z\2\2\u0177\u0178")
        buf.write("\7v\2\2\u0178@\3\2\2\2\u0179\u017a\7i\2\2\u017a\u017b")
        buf.write("\7g\2\2\u017b\u017c\7v\2\2\u017c\u017d\7a\2\2\u017d\u017e")
        buf.write("\7k\2\2\u017e\u017f\7f\2\2\u017f\u0180\7g\2\2\u0180\u0181")
        buf.write("\7p\2\2\u0181\u0182\7v\2\2\u0182B\3\2\2\2\u0183\u0184")
        buf.write("\7j\2\2\u0184\u0185\7c\2\2\u0185\u0186\7u\2\2\u0186\u0187")
        buf.write("\7j\2\2\u0187D\3\2\2\2\u0188\u0189\7j\2\2\u0189\u018a")
        buf.write("\7g\2\2\u018a\u018b\7z\2\2\u018bF\3\2\2\2\u018c\u018d")
        buf.write("\7k\2\2\u018d\u018e\7p\2\2\u018e\u018f\7v\2\2\u018fH\3")
        buf.write("\2\2\2\u0190\u0191\7m\2\2\u0191\u0192\7g\2\2\u0192\u0193")
        buf.write("\7{\2\2\u0193\u0194\7u\2\2\u0194J\3\2\2\2\u0195\u0196")
        buf.write("\7n\2\2\u0196\u0197\7g\2\2\u0197\u0198\7p\2\2\u0198L\3")
        buf.write("\2\2\2\u0199\u019a\7n\2\2\u019a\u019b\7k\2\2\u019b\u019c")
        buf.write("\7u\2\2\u019c\u019d\7v\2\2\u019dN\3\2\2\2\u019e\u019f")
        buf.write("\7o\2\2\u019f\u01a0\7c\2\2\u01a0\u01a1\7z\2\2\u01a1P\3")
        buf.write("\2\2\2\u01a2\u01a3\7o\2\2\u01a3\u01a4\7k\2\2\u01a4\u01a5")
        buf.write("\7p\2\2\u01a5R\3\2\2\2\u01a6\u01a7\7t\2\2\u01a7\u01a8")
        buf.write("\7g\2\2\u01a8\u01a9\7x\2\2\u01a9\u01aa\7g\2\2\u01aa\u01ab")
        buf.write("\7t\2\2\u01ab\u01ac\7u\2\2\u01ac\u01ad\7g\2\2\u01ad\u01ae")
        buf.write("\7f\2\2\u01aeT\3\2\2\2\u01af\u01b0\7u\2\2\u01b0\u01b1")
        buf.write("\7g\2\2\u01b1\u01b2\7v\2\2\u01b2V\3\2\2\2\u01b3\u01b4")
        buf.write("\7u\2\2\u01b4\u01b5\7q\2\2\u01b5\u01b6\7t\2\2\u01b6\u01b7")
        buf.write("\7v\2\2\u01b7\u01b8\7g\2\2\u01b8\u01b9\7f\2\2\u01b9X\3")
        buf.write("\2\2\2\u01ba\u01bb\7u\2\2\u01bb\u01bc\7v\2\2\u01bc\u01bd")
        buf.write("\7t\2\2\u01bdZ\3\2\2\2\u01be\u01bf\7u\2\2\u01bf\u01c0")
        buf.write("\7w\2\2\u01c0\u01c1\7o\2\2\u01c1\\\3\2\2\2\u01c2\u01c3")
        buf.write("\7v\2\2\u01c3\u01c4\7{\2\2\u01c4\u01c5\7r\2\2\u01c5\u01c6")
        buf.write("\7g\2\2\u01c6^\3\2\2\2\u01c7\u01c8\7g\2\2\u01c8\u01c9")
        buf.write("\7p\2\2\u01c9\u01ca\7f\2\2\u01ca`\3\2\2\2\u01cb\u01cc")
        buf.write("\7c\2\2\u01cc\u01cd\7p\2\2\u01cd\u01ce\7f\2\2\u01ce\u01cf")
        buf.write("\7?\2\2\u01cfb\3\2\2\2\u01d0\u01d1\7q\2\2\u01d1\u01d2")
        buf.write("\7t\2\2\u01d2\u01d3\7?\2\2\u01d3d\3\2\2\2\u01d4\u01d5")
        buf.write("\7?\2\2\u01d5\u01d6\7@\2\2\u01d6\u01d7\7?\2\2\u01d7f\3")
        buf.write("\2\2\2\u01d8\u01d9\7(\2\2\u01d9\u01da\7?\2\2\u01dah\3")
        buf.write("\2\2\2\u01db\u01dc\7~\2\2\u01dc\u01dd\7?\2\2\u01ddj\3")
        buf.write("\2\2\2\u01de\u01df\7`\2\2\u01df\u01e0\7?\2\2\u01e0l\3")
        buf.write("\2\2\2\u01e1\u01e2\7/\2\2\u01e2\u01e3\7?\2\2\u01e3n\3")
        buf.write("\2\2\2\u01e4\u01e5\7-\2\2\u01e5\u01e6\7?\2\2\u01e6p\3")
        buf.write("\2\2\2\u01e7\u01e8\7,\2\2\u01e8\u01e9\7?\2\2\u01e9r\3")
        buf.write("\2\2\2\u01ea\u01eb\7\61\2\2\u01eb\u01ec\7?\2\2\u01ect")
        buf.write("\3\2\2\2\u01ed\u01ee\7\61\2\2\u01ee\u01ef\7\61\2\2\u01ef")
        buf.write("\u01f0\7?\2\2\u01f0v\3\2\2\2\u01f1\u01f2\7\'\2\2\u01f2")
        buf.write("\u01f3\7?\2\2\u01f3x\3\2\2\2\u01f4\u01f5\7o\2\2\u01f5")
        buf.write("\u01f6\7q\2\2\u01f6\u01f7\7f\2\2\u01f7\u01f8\7?\2\2\u01f8")
        buf.write("z\3\2\2\2\u01f9\u01fa\7,\2\2\u01fa\u01fb\7,\2\2\u01fb")
        buf.write("\u01fc\7?\2\2\u01fc|\3\2\2\2\u01fd\u01fe\7@\2\2\u01fe")
        buf.write("\u01ff\7@\2\2\u01ff\u0200\7?\2\2\u0200~\3\2\2\2\u0201")
        buf.write("\u0202\7>\2\2\u0202\u0203\7>\2\2\u0203\u0204\7?\2\2\u0204")
        buf.write("\u0080\3\2\2\2\u0205\u0207\7\17\2\2\u0206\u0205\3\2\2")
        buf.write("\2\u0206\u0207\3\2\2\2\u0207\u0208\3\2\2\2\u0208\u0215")
        buf.write("\7\f\2\2\u0209\u020b\7\"\2\2\u020a\u0209\3\2\2\2\u020b")
        buf.write("\u020e\3\2\2\2\u020c\u020a\3\2\2\2\u020c\u020d\3\2\2\2")
        buf.write("\u020d\u0216\3\2\2\2\u020e\u020c\3\2\2\2\u020f\u0211\7")
        buf.write("\13\2\2\u0210\u020f\3\2\2\2\u0211\u0214\3\2\2\2\u0212")
        buf.write("\u0210\3\2\2\2\u0212\u0213\3\2\2\2\u0213\u0216\3\2\2\2")
        buf.write("\u0214\u0212\3\2\2\2\u0215\u020c\3\2\2\2\u0215\u0212\3")
        buf.write("\2\2\2\u0216\u0217\3\2\2\2\u0217\u0218\bA\2\2\u0218\u0082")
        buf.write("\3\2\2\2\u0219\u021b\7\"\2\2\u021a\u0219\3\2\2\2\u021b")
        buf.write("\u021c\3\2\2\2\u021c\u021a\3\2\2\2\u021c\u021d\3\2\2\2")
        buf.write("\u021d\u0227\3\2\2\2\u021e\u0220\7\13\2\2\u021f\u021e")
        buf.write("\3\2\2\2\u0220\u0221\3\2\2\2\u0221\u021f\3\2\2\2\u0221")
        buf.write("\u0222\3\2\2\2\u0222\u0227\3\2\2\2\u0223\u0224\7^\2\2")
        buf.write("\u0224\u0227\5\u0081A\2\u0225\u0227\5\u0085C\2\u0226\u021a")
        buf.write("\3\2\2\2\u0226\u021f\3\2\2\2\u0226\u0223\3\2\2\2\u0226")
        buf.write("\u0225\3\2\2\2\u0227\u0228\3\2\2\2\u0228\u0229\bB\3\2")
        buf.write("\u0229\u0084\3\2\2\2\u022a\u022e\5\u0089E\2\u022b\u022d")
        buf.write("\13\2\2\2\u022c\u022b\3\2\2\2\u022d\u0230\3\2\2\2\u022e")
        buf.write("\u022f\3\2\2\2\u022e\u022c\3\2\2\2\u022f\u0231\3\2\2\2")
        buf.write("\u0230\u022e\3\2\2\2\u0231\u0232\5\u008bF\2\u0232\u023b")
        buf.write("\3\2\2\2\u0233\u0237\5\u0087D\2\u0234\u0236\n\2\2\2\u0235")
        buf.write("\u0234\3\2\2\2\u0236\u0239\3\2\2\2\u0237\u0235\3\2\2\2")
        buf.write("\u0237\u0238\3\2\2\2\u0238\u023b\3\2\2\2\u0239\u0237\3")
        buf.write("\2\2\2\u023a\u022a\3\2\2\2\u023a\u0233\3\2\2\2\u023b\u0086")
        buf.write("\3\2\2\2\u023c\u023d\7%\2\2\u023d\u0088\3\2\2\2\u023e")
        buf.write("\u023f\7*\2\2\u023f\u0240\7,\2\2\u0240\u008a\3\2\2\2\u0241")
        buf.write("\u0242\7,\2\2\u0242\u0243\7+\2\2\u0243\u008c\3\2\2\2\u0244")
        buf.write("\u0245\7,\2\2\u0245\u008e\3\2\2\2\u0246\u0247\7c\2\2\u0247")
        buf.write("\u0248\7u\2\2\u0248\u0090\3\2\2\2\u0249\u024a\7\60\2\2")
        buf.write("\u024a\u0092\3\2\2\2\u024b\u024c\7k\2\2\u024c\u024d\7")
        buf.write("o\2\2\u024d\u024e\7r\2\2\u024e\u024f\7q\2\2\u024f\u0250")
        buf.write("\7t\2\2\u0250\u0251\7v\2\2\u0251\u0094\3\2\2\2\u0252\u0253")
        buf.write("\7r\2\2\u0253\u0254\7t\2\2\u0254\u0255\7k\2\2\u0255\u0256")
        buf.write("\7p\2\2\u0256\u0257\7v\2\2\u0257\u0096\3\2\2\2\u0258\u0259")
        buf.write("\7h\2\2\u0259\u025a\7t\2\2\u025a\u025b\7q\2\2\u025b\u025c")
        buf.write("\7o\2\2\u025c\u0098\3\2\2\2\u025d\u025e\7\60\2\2\u025e")
        buf.write("\u025f\7\60\2\2\u025f\u009a\3\2\2\2\u0260\u0261\7u\2\2")
        buf.write("\u0261\u0262\7g\2\2\u0262\u0263\7v\2\2\u0263\u0264\7k")
        buf.write("\2\2\u0264\u0265\7p\2\2\u0265\u0266\7v\2\2\u0266\u0267")
        buf.write("\7n\2\2\u0267\u0268\7g\2\2\u0268\u0269\7x\2\2\u0269\u026a")
        buf.write("\7g\2\2\u026a\u026b\7n\2\2\u026b\u009c\3\2\2\2\u026c\u026d")
        buf.write("\7u\2\2\u026d\u026e\7c\2\2\u026e\u026f\7x\2\2\u026f\u0270")
        buf.write("\7g\2\2\u0270\u009e\3\2\2\2\u0271\u0272\7u\2\2\u0272\u0273")
        buf.write("\7v\2\2\u0273\u0274\7q\2\2\u0274\u0275\7r\2\2\u0275\u00a0")
        buf.write("\3\2\2\2\u0276\u0277\7n\2\2\u0277\u0278\7c\2\2\u0278\u0279")
        buf.write("\7o\2\2\u0279\u027a\7d\2\2\u027a\u027b\7f\2\2\u027b\u027c")
        buf.write("\7c\2\2\u027c\u00a2\3\2\2\2\u027d\u027e\7p\2\2\u027e\u027f")
        buf.write("\7q\2\2\u027f\u0280\7v\2\2\u0280\u00a4\3\2\2\2\u0281\u0282")
        buf.write("\7.\2\2\u0282\u00a6\3\2\2\2\u0283\u0284\7e\2\2\u0284\u0285")
        buf.write("\7q\2\2\u0285\u0286\7p\2\2\u0286\u0287\7u\2\2\u0287\u0288")
        buf.write("\7v\2\2\u0288\u00a8\3\2\2\2\u0289\u028a\7c\2\2\u028a\u028b")
        buf.write("\7y\2\2\u028b\u028c\7c\2\2\u028c\u028d\7k\2\2\u028d\u028e")
        buf.write("\7v\2\2\u028e\u00aa\3\2\2\2\u028f\u0290\7c\2\2\u0290\u0291")
        buf.write("\7u\2\2\u0291\u0292\7u\2\2\u0292\u0293\7g\2\2\u0293\u0294")
        buf.write("\7t\2\2\u0294\u0295\7v\2\2\u0295\u00ac\3\2\2\2\u0296\u0297")
        buf.write("\7x\2\2\u0297\u0298\7c\2\2\u0298\u0299\7t\2\2\u0299\u00ae")
        buf.write("\3\2\2\2\u029a\u029b\7v\2\2\u029b\u029c\7t\2\2\u029c\u029d")
        buf.write("\7c\2\2\u029d\u029e\7r\2\2\u029e\u00b0\3\2\2\2\u029f\u02a0")
        buf.write("\7r\2\2\u02a0\u02a1\7c\2\2\u02a1\u02a2\7u\2\2\u02a2\u02a3")
        buf.write("\7u\2\2\u02a3\u00b2\3\2\2\2\u02a4\u02a5\7f\2\2\u02a5\u02a6")
        buf.write("\7g\2\2\u02a6\u02a7\7n\2\2\u02a7\u00b4\3\2\2\2\u02a8\u02a9")
        buf.write("\7u\2\2\u02a9\u02aa\7r\2\2\u02aa\u02ab\7c\2\2\u02ab\u02ac")
        buf.write("\7y\2\2\u02ac\u02ad\7p\2\2\u02ad\u00b6\3\2\2\2\u02ae\u02af")
        buf.write("\7h\2\2\u02af\u02b0\7k\2\2\u02b0\u02b1\7p\2\2\u02b1\u02b2")
        buf.write("\7c\2\2\u02b2\u02b3\7n\2\2\u02b3\u02b4\7n\2\2\u02b4\u02b5")
        buf.write("\7{\2\2\u02b5\u00b8\3\2\2\2\u02b6\u02b7\7k\2\2\u02b7\u02b8")
        buf.write("\7p\2\2\u02b8\u02b9\7x\2\2\u02b9\u02ba\7c\2\2\u02ba\u02bb")
        buf.write("\7t\2\2\u02bb\u02bc\7k\2\2\u02bc\u02bd\7c\2\2\u02bd\u02be")
        buf.write("\7p\2\2\u02be\u02bf\7v\2\2\u02bf\u00ba\3\2\2\2\u02c0\u02c1")
        buf.write("\7i\2\2\u02c1\u02c2\7q\2\2\u02c2\u00bc\3\2\2\2\u02c3\u02c4")
        buf.write("\7d\2\2\u02c4\u02c5\7w\2\2\u02c5\u02c6\7k\2\2\u02c6\u02c7")
        buf.write("\7n\2\2\u02c7\u02c8\7v\2\2\u02c8\u02c9\7k\2\2\u02c9\u02ca")
        buf.write("\7p\2\2\u02ca\u00be\3\2\2\2\u02cb\u02cc\7u\2\2\u02cc\u02cd")
        buf.write("\7g\2\2\u02cd\u02ce\7s\2\2\u02ce\u02cf\7w\2\2\u02cf\u02d0")
        buf.write("\7g\2\2\u02d0\u02d1\7p\2\2\u02d1\u02d2\7v\2\2\u02d2\u02d3")
        buf.write("\7k\2\2\u02d3\u02d4\7c\2\2\u02d4\u02d5\7n\2\2\u02d5\u00c0")
        buf.write("\3\2\2\2\u02d6\u02d7\7y\2\2\u02d7\u02d8\7j\2\2\u02d8\u02d9")
        buf.write("\7g\2\2\u02d9\u02da\7p\2\2\u02da\u00c2\3\2\2\2\u02db\u02dc")
        buf.write("\7n\2\2\u02dc\u02dd\7g\2\2\u02dd\u02de\7v\2\2\u02de\u00c4")
        buf.write("\3\2\2\2\u02df\u02e0\7k\2\2\u02e0\u02e1\7h\2\2\u02e1\u00c6")
        buf.write("\3\2\2\2\u02e2\u02e3\7g\2\2\u02e3\u02e4\7n\2\2\u02e4\u02e5")
        buf.write("\7k\2\2\u02e5\u02e6\7h\2\2\u02e6\u00c8\3\2\2\2\u02e7\u02e8")
        buf.write("\7g\2\2\u02e8\u02e9\7n\2\2\u02e9\u02ea\7u\2\2\u02ea\u02eb")
        buf.write("\7g\2\2\u02eb\u00ca\3\2\2\2\u02ec\u02ed\7B\2\2\u02ed\u00cc")
        buf.write("\3\2\2\2\u02ee\u02ef\7y\2\2\u02ef\u02f0\7j\2\2\u02f0\u02f1")
        buf.write("\7k\2\2\u02f1\u02f2\7n\2\2\u02f2\u02f3\7g\2\2\u02f3\u00ce")
        buf.write("\3\2\2\2\u02f4\u02f5\7i\2\2\u02f5\u02f6\7n\2\2\u02f6\u02f7")
        buf.write("\7q\2\2\u02f7\u02f8\7d\2\2\u02f8\u02f9\7c\2\2\u02f9\u02fa")
        buf.write("\7n\2\2\u02fa\u00d0\3\2\2\2\u02fb\u02fc\7f\2\2\u02fc\u02fd")
        buf.write("\7g\2\2\u02fd\u02fe\7h\2\2\u02fe\u00d2\3\2\2\2\u02ff\u0300")
        buf.write("\7t\2\2\u0300\u0301\7g\2\2\u0301\u0302\7v\2\2\u0302\u0303")
        buf.write("\7w\2\2\u0303\u0304\7t\2\2\u0304\u0305\7p\2\2\u0305\u0306")
        buf.write("\7u\2\2\u0306\u00d4\3\2\2\2\u0307\u0308\7g\2\2\u0308\u0309")
        buf.write("\7z\2\2\u0309\u030a\7k\2\2\u030a\u030b\7u\2\2\u030b\u030c")
        buf.write("\7v\2\2\u030c\u030d\7u\2\2\u030d\u00d6\3\2\2\2\u030e\u030f")
        buf.write("\7y\2\2\u030f\u0310\7j\2\2\u0310\u0311\7g\2\2\u0311\u0312")
        buf.write("\7t\2\2\u0312\u0313\7g\2\2\u0313\u00d8\3\2\2\2\u0314\u0315")
        buf.write("\7?\2\2\u0315\u00da\3\2\2\2\u0316\u0317\7h\2\2\u0317\u0318")
        buf.write("\7q\2\2\u0318\u0319\7t\2\2\u0319\u031a\3\2\2\2\u031a\u031b")
        buf.write("\bn\4\2\u031b\u00dc\3\2\2\2\u031c\u031d\7k\2\2\u031d\u031e")
        buf.write("\7p\2\2\u031e\u031f\3\2\2\2\u031f\u0320\bo\5\2\u0320\u00de")
        buf.write("\3\2\2\2\u0321\u0322\7<\2\2\u0322\u00e0\3\2\2\2\u0323")
        buf.write("\u0324\7P\2\2\u0324\u0325\7q\2\2\u0325\u0326\7p\2\2\u0326")
        buf.write("\u0327\7g\2\2\u0327\u00e2\3\2\2\2\u0328\u0329\7c\2\2\u0329")
        buf.write("\u032a\7v\2\2\u032a\u032b\7q\2\2\u032b\u032c\7o\2\2\u032c")
        buf.write("\u032d\7k\2\2\u032d\u032e\7e\2\2\u032e\u032f\7c\2\2\u032f")
        buf.write("\u0330\7n\2\2\u0330\u0331\7n\2\2\u0331\u0332\7{\2\2\u0332")
        buf.write("\u00e4\3\2\2\2\u0333\u0334\7H\2\2\u0334\u0335\7c\2\2\u0335")
        buf.write("\u0336\7n\2\2\u0336\u0337\7u\2\2\u0337\u033d\7g\2\2\u0338")
        buf.write("\u0339\7V\2\2\u0339\u033a\7t\2\2\u033a\u033b\7w\2\2\u033b")
        buf.write("\u033d\7g\2\2\u033c\u0333\3\2\2\2\u033c\u0338\3\2\2\2")
        buf.write("\u033d\u00e6\3\2\2\2\u033e\u033f\7g\2\2\u033f\u0340\7")
        buf.write("v\2\2\u0340\u0341\7g\2\2\u0341\u0342\7t\2\2\u0342\u0343")
        buf.write("\7p\2\2\u0343\u0344\7c\2\2\u0344\u0345\7n\2\2\u0345\u00e8")
        buf.write("\3\2\2\2\u0346\u0348\t\3\2\2\u0347\u0346\3\2\2\2\u0348")
        buf.write("\u0349\3\2\2\2\u0349\u0347\3\2\2\2\u0349\u034a\3\2\2\2")
        buf.write("\u034a\u0364\3\2\2\2\u034b\u034c\7\62\2\2\u034c\u034d")
        buf.write("\7z\2\2\u034d\u034f\3\2\2\2\u034e\u0350\t\4\2\2\u034f")
        buf.write("\u034e\3\2\2\2\u0350\u0351\3\2\2\2\u0351\u034f\3\2\2\2")
        buf.write("\u0351\u0352\3\2\2\2\u0352\u0364\3\2\2\2\u0353\u0354\7")
        buf.write("\62\2\2\u0354\u0355\7d\2\2\u0355\u0357\3\2\2\2\u0356\u0358")
        buf.write("\t\5\2\2\u0357\u0356\3\2\2\2\u0358\u0359\3\2\2\2\u0359")
        buf.write("\u0357\3\2\2\2\u0359\u035a\3\2\2\2\u035a\u0364\3\2\2\2")
        buf.write("\u035b\u035c\7\62\2\2\u035c\u035d\7q\2\2\u035d\u035f\3")
        buf.write("\2\2\2\u035e\u0360\t\6\2\2\u035f\u035e\3\2\2\2\u0360\u0361")
        buf.write("\3\2\2\2\u0361\u035f\3\2\2\2\u0361\u0362\3\2\2\2\u0362")
        buf.write("\u0364\3\2\2\2\u0363\u0347\3\2\2\2\u0363\u034b\3\2\2\2")
        buf.write("\u0363\u0353\3\2\2\2\u0363\u035b\3\2\2\2\u0364\u00ea\3")
        buf.write("\2\2\2\u0365\u0369\t\7\2\2\u0366\u0368\t\b\2\2\u0367\u0366")
        buf.write("\3\2\2\2\u0368\u036b\3\2\2\2\u0369\u0367\3\2\2\2\u0369")
        buf.write("\u036a\3\2\2\2\u036a\u00ec\3\2\2\2\u036b\u0369\3\2\2\2")
        buf.write("\u036c\u036f\t\t\2\2\u036d\u0370\5\u00f1y\2\u036e\u0370")
        buf.write("\5\u00ebv\2\u036f\u036d\3\2\2\2\u036f\u036e\3\2\2\2\u0370")
        buf.write("\u00ee\3\2\2\2\u0371\u0372\7/\2\2\u0372\u0373\7@\2\2\u0373")
        buf.write("\u0377\3\2\2\2\u0374\u0376\7\"\2\2\u0375\u0374\3\2\2\2")
        buf.write("\u0376\u0379\3\2\2\2\u0377\u0375\3\2\2\2\u0377\u0378\3")
        buf.write("\2\2\2\u0378\u037a\3\2\2\2\u0379\u0377\3\2\2\2\u037a\u037b")
        buf.write("\5\u00ebv\2\u037b\u00f0\3\2\2\2\u037c\u037d\7\62\2\2\u037d")
        buf.write("\u037e\7Z\2\2\u037e\u0380\3\2\2\2\u037f\u0381\5\u00f3")
        buf.write("z\2\u0380\u037f\3\2\2\2\u0381\u0382\3\2\2\2\u0382\u0380")
        buf.write("\3\2\2\2\u0382\u0383\3\2\2\2\u0383\u00f2\3\2\2\2\u0384")
        buf.write("\u0385\t\4\2\2\u0385\u00f4\3\2\2\2\u0386\u0387\7]\2\2")
        buf.write("\u0387\u0388\b{\6\2\u0388\u00f6\3\2\2\2\u0389\u038a\7")
        buf.write("_\2\2\u038a\u038b\b|\7\2\u038b\u00f8\3\2\2\2\u038c\u038d")
        buf.write("\7}\2\2\u038d\u038e\b}\b\2\u038e\u00fa\3\2\2\2\u038f\u0390")
        buf.write("\7\177\2\2\u0390\u0391\b~\t\2\u0391\u00fc\3\2\2\2\u0392")
        buf.write("\u0393\7*\2\2\u0393\u0394\b\177\n\2\u0394\u00fe\3\2\2")
        buf.write("\2\u0395\u0396\7+\2\2\u0396\u0397\b\u0080\13\2\u0397\u0100")
        buf.write("\3\2\2\2\u0398\u0399\7=\2\2\u0399\u0102\3\2\2\2\u039a")
        buf.write("\u039d\5\u0105\u0083\2\u039b\u039d\5\u0107\u0084\2\u039c")
        buf.write("\u039a\3\2\2\2\u039c\u039b\3\2\2\2\u039d\u0104\3\2\2\2")
        buf.write("\u039e\u03a3\7)\2\2\u039f\u03a2\5\u010d\u0087\2\u03a0")
        buf.write("\u03a2\n\n\2\2\u03a1\u039f\3\2\2\2\u03a1\u03a0\3\2\2\2")
        buf.write("\u03a2\u03a5\3\2\2\2\u03a3\u03a1\3\2\2\2\u03a3\u03a4\3")
        buf.write("\2\2\2\u03a4\u03a6\3\2\2\2\u03a5\u03a3\3\2\2\2\u03a6\u03b1")
        buf.write("\7)\2\2\u03a7\u03ac\7$\2\2\u03a8\u03ab\5\u010d\u0087\2")
        buf.write("\u03a9\u03ab\n\13\2\2\u03aa\u03a8\3\2\2\2\u03aa\u03a9")
        buf.write("\3\2\2\2\u03ab\u03ae\3\2\2\2\u03ac\u03aa\3\2\2\2\u03ac")
        buf.write("\u03ad\3\2\2\2\u03ad\u03af\3\2\2\2\u03ae\u03ac\3\2\2\2")
        buf.write("\u03af\u03b1\7$\2\2\u03b0\u039e\3\2\2\2\u03b0\u03a7\3")
        buf.write("\2\2\2\u03b1\u0106\3\2\2\2\u03b2\u03b3\7)\2\2\u03b3\u03b4")
        buf.write("\7)\2\2\u03b4\u03b5\7)\2\2\u03b5\u03b9\3\2\2\2\u03b6\u03b8")
        buf.write("\5\u0109\u0085\2\u03b7\u03b6\3\2\2\2\u03b8\u03bb\3\2\2")
        buf.write("\2\u03b9\u03ba\3\2\2\2\u03b9\u03b7\3\2\2\2\u03ba\u03bc")
        buf.write("\3\2\2\2\u03bb\u03b9\3\2\2\2\u03bc\u03bd\7)\2\2\u03bd")
        buf.write("\u03be\7)\2\2\u03be\u03cd\7)\2\2\u03bf\u03c0\7$\2\2\u03c0")
        buf.write("\u03c1\7$\2\2\u03c1\u03c2\7$\2\2\u03c2\u03c6\3\2\2\2\u03c3")
        buf.write("\u03c5\5\u0109\u0085\2\u03c4\u03c3\3\2\2\2\u03c5\u03c8")
        buf.write("\3\2\2\2\u03c6\u03c7\3\2\2\2\u03c6\u03c4\3\2\2\2\u03c7")
        buf.write("\u03c9\3\2\2\2\u03c8\u03c6\3\2\2\2\u03c9\u03ca\7$\2\2")
        buf.write("\u03ca\u03cb\7$\2\2\u03cb\u03cd\7$\2\2\u03cc\u03b2\3\2")
        buf.write("\2\2\u03cc\u03bf\3\2\2\2\u03cd\u0108\3\2\2\2\u03ce\u03d1")
        buf.write("\5\u010b\u0086\2\u03cf\u03d1\5\u010d\u0087\2\u03d0\u03ce")
        buf.write("\3\2\2\2\u03d0\u03cf\3\2\2\2\u03d1\u010a\3\2\2\2\u03d2")
        buf.write("\u03d3\n\f\2\2\u03d3\u010c\3\2\2\2\u03d4\u03d5\7^\2\2")
        buf.write("\u03d5\u03d9\13\2\2\2\u03d6\u03d7\7^\2\2\u03d7\u03d9\5")
        buf.write("\u0081A\2\u03d8\u03d4\3\2\2\2\u03d8\u03d6\3\2\2\2\u03d9")
        buf.write("\u010e\3\2\2\2\"\2\u0206\u020c\u0212\u0215\u021c\u0221")
        buf.write("\u0226\u022e\u0237\u023a\u033c\u0349\u0351\u0359\u0361")
        buf.write("\u0363\u0369\u036f\u0377\u0382\u039c\u03a1\u03a3\u03aa")
        buf.write("\u03ac\u03b0\u03b9\u03c6\u03cc\u03d0\u03d8\f\3A\2\b\2")
        buf.write("\2\3n\3\3o\4\3{\5\3|\6\3}\7\3~\b\3\177\t\3\u0080\n")
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
    T__53 = 54
    T__54 = 55
    T__55 = 56
    T__56 = 57
    T__57 = 58
    T__58 = 59
    T__59 = 60
    T__60 = 61
    T__61 = 62
    T__62 = 63
    NL = 64
    WS = 65
    COMMENT_START = 66
    OPEN_MULTI_COMMENT = 67
    CLOSE_MULTI_COMMENT = 68
    STAR = 69
    AS = 70
    DOT = 71
    IMPORT = 72
    PRINT = 73
    FROM = 74
    RANGE = 75
    SETINTLEVEL = 76
    SAVE = 77
    STOP = 78
    LAMBDA = 79
    NOT = 80
    COMMA = 81
    CONST = 82
    AWAIT = 83
    ASSERT = 84
    VAR = 85
    TRAP = 86
    PASS = 87
    DEL = 88
    SPAWN = 89
    FINALLY = 90
    INVARIANT = 91
    GO = 92
    BUILTIN = 93
    SEQUENTIAL = 94
    WHEN = 95
    LET = 96
    IF = 97
    ELIF = 98
    ELSE = 99
    AT = 100
    WHILE = 101
    GLOBAL = 102
    DEF = 103
    RETURNS = 104
    EXISTS = 105
    WHERE = 106
    EQ = 107
    FOR = 108
    IN = 109
    COLON = 110
    NONE = 111
    ATOMICALLY = 112
    BOOL = 113
    ETERNAL = 114
    INT = 115
    NAME = 116
    ATOM = 117
    ARROWID = 118
    HEX_INTEGER = 119
    OPEN_BRACK = 120
    CLOSE_BRACK = 121
    OPEN_BRACES = 122
    CLOSE_BRACES = 123
    OPEN_PAREN = 124
    CLOSE_PAREN = 125
    SEMI_COLON = 126
    STRING = 127

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'or'", "'&'", "'|'", "'^'", "'-'", "'+'", "'//'", 
            "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", "'!='", 
            "'<'", "'<='", "'>'", "'>='", "'=>'", "'~'", "'?'", "'!'", "'abs'", 
            "'all'", "'any'", "'bin'", "'choose'", "'contexts'", "'get_context'", 
            "'get_ident'", "'hash'", "'hex'", "'int'", "'keys'", "'len'", 
            "'list'", "'max'", "'min'", "'reversed'", "'set'", "'sorted'", 
            "'str'", "'sum'", "'type'", "'end'", "'and='", "'or='", "'=>='", 
            "'&='", "'|='", "'^='", "'-='", "'+='", "'*='", "'/='", "'//='", 
            "'%='", "'mod='", "'**='", "'>>='", "'<<='", "'#'", "'(*'", 
            "'*)'", "'*'", "'as'", "'.'", "'import'", "'print'", "'from'", 
            "'..'", "'setintlevel'", "'save'", "'stop'", "'lambda'", "'not'", 
            "','", "'const'", "'await'", "'assert'", "'var'", "'trap'", 
            "'pass'", "'del'", "'spawn'", "'finally'", "'invariant'", "'go'", 
            "'builtin'", "'sequential'", "'when'", "'let'", "'if'", "'elif'", 
            "'else'", "'@'", "'while'", "'global'", "'def'", "'returns'", 
            "'exists'", "'where'", "'='", "'for'", "'in'", "':'", "'None'", 
            "'atomically'", "'eternal'", "'['", "']'", "'{'", "'}'", "'('", 
            "')'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "NL", "WS", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
            "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", "RANGE", "SETINTLEVEL", 
            "SAVE", "STOP", "LAMBDA", "NOT", "COMMA", "CONST", "AWAIT", 
            "ASSERT", "VAR", "TRAP", "PASS", "DEL", "SPAWN", "FINALLY", 
            "INVARIANT", "GO", "BUILTIN", "SEQUENTIAL", "WHEN", "LET", "IF", 
            "ELIF", "ELSE", "AT", "WHILE", "GLOBAL", "DEF", "RETURNS", "EXISTS", 
            "WHERE", "EQ", "FOR", "IN", "COLON", "NONE", "ATOMICALLY", "BOOL", 
            "ETERNAL", "INT", "NAME", "ATOM", "ARROWID", "HEX_INTEGER", 
            "OPEN_BRACK", "CLOSE_BRACK", "OPEN_BRACES", "CLOSE_BRACES", 
            "OPEN_PAREN", "CLOSE_PAREN", "SEMI_COLON", "STRING" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "T__20", "T__21", "T__22", "T__23", "T__24", "T__25", 
                  "T__26", "T__27", "T__28", "T__29", "T__30", "T__31", 
                  "T__32", "T__33", "T__34", "T__35", "T__36", "T__37", 
                  "T__38", "T__39", "T__40", "T__41", "T__42", "T__43", 
                  "T__44", "T__45", "T__46", "T__47", "T__48", "T__49", 
                  "T__50", "T__51", "T__52", "T__53", "T__54", "T__55", 
                  "T__56", "T__57", "T__58", "T__59", "T__60", "T__61", 
                  "T__62", "NL", "WS", "COMMENT", "COMMENT_START", "OPEN_MULTI_COMMENT", 
                  "CLOSE_MULTI_COMMENT", "STAR", "AS", "DOT", "IMPORT", 
                  "PRINT", "FROM", "RANGE", "SETINTLEVEL", "SAVE", "STOP", 
                  "LAMBDA", "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", 
                  "VAR", "TRAP", "PASS", "DEL", "SPAWN", "FINALLY", "INVARIANT", 
                  "GO", "BUILTIN", "SEQUENTIAL", "WHEN", "LET", "IF", "ELIF", 
                  "ELSE", "AT", "WHILE", "GLOBAL", "DEF", "RETURNS", "EXISTS", 
                  "WHERE", "EQ", "FOR", "IN", "COLON", "NONE", "ATOMICALLY", 
                  "BOOL", "ETERNAL", "INT", "NAME", "ATOM", "ARROWID", "HEX_INTEGER", 
                  "HEX_DIGIT", "OPEN_BRACK", "CLOSE_BRACK", "OPEN_BRACES", 
                  "CLOSE_BRACES", "OPEN_PAREN", "CLOSE_PAREN", "SEMI_COLON", 
                  "STRING", "SHORT_STRING", "LONG_STRING", "LONG_STRING_ITEM", 
                  "LONG_STRING_CHAR", "STRING_ESCAPE_SEQ" ]

    grammarFileName = "Harmony.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None



    opened_for = 0
    opened = 0

    class HarmonyDenter(ModifiedDenterHelper):
        def __init__(self, lexer, nl_token, colon_token, indent_token, dedent_token, ignore_eof):
            super().__init__(lexer, nl_token, colon_token, indent_token, dedent_token, ignore_eof)
            self.lexer: HarmonyLexer = lexer

        def pull_token(self):
            return super(HarmonyLexer, self.lexer).nextToken()

    denter = None
    def nextToken(self):
        if not self.denter:
            self.denter = self.HarmonyDenter(self, self.NL, self.COLON, HarmonyParser.INDENT, HarmonyParser.DEDENT, ignore_eof=False)
        token = self.denter.next_token()
        return token


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[63] = self.NL_action 
            actions[108] = self.FOR_action 
            actions[109] = self.IN_action 
            actions[121] = self.OPEN_BRACK_action 
            actions[122] = self.CLOSE_BRACK_action 
            actions[123] = self.OPEN_BRACES_action 
            actions[124] = self.CLOSE_BRACES_action 
            actions[125] = self.OPEN_PAREN_action 
            actions[126] = self.CLOSE_PAREN_action 
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

            if self.opened_for > 0:
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
     


