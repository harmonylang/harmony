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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2}")
        buf.write("\u03c4\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3")
        buf.write("\7\3\7\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3")
        buf.write("\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3\17\3\20")
        buf.write("\3\20\3\20\3\21\3\21\3\21\3\22\3\22\3\23\3\23\3\23\3\24")
        buf.write("\3\24\3\25\3\25\3\25\3\26\3\26\3\27\3\27\3\30\3\30\3\31")
        buf.write("\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\33")
        buf.write("\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\35\3\35\3\35")
        buf.write("\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37")
        buf.write("\3\37\3\37\3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3!\3!\3")
        buf.write("!\3!\3!\3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3\"\3#\3#\3#\3")
        buf.write("#\3#\3$\3$\3$\3$\3%\3%\3%\3%\3&\3&\3&\3&\3\'\3\'\3\'\3")
        buf.write("\'\3(\3(\3(\3(\3)\3)\3)\3)\3*\3*\3*\3*\3*\3+\3+\3+\3+")
        buf.write("\3,\3,\3,\3,\3,\3-\3-\3-\3-\3.\3.\3.\3.\3/\3/\3/\3\60")
        buf.write("\3\60\3\60\3\61\3\61\3\61\3\62\3\62\3\62\3\63\3\63\3\63")
        buf.write("\3\64\3\64\3\64\3\65\3\65\3\65\3\66\3\66\3\66\3\66\3\67")
        buf.write("\3\67\3\67\38\38\38\38\38\39\39\39\39\3:\3:\3:\3:\3;\3")
        buf.write(";\3;\3;\3<\5<\u01ee\n<\3<\3<\7<\u01f2\n<\f<\16<\u01f5")
        buf.write("\13<\3<\7<\u01f8\n<\f<\16<\u01fb\13<\5<\u01fd\n<\3<\3")
        buf.write("<\3=\6=\u0202\n=\r=\16=\u0203\3=\6=\u0207\n=\r=\16=\u0208")
        buf.write("\3=\3=\3=\5=\u020e\n=\3=\3=\3>\3>\7>\u0214\n>\f>\16>\u0217")
        buf.write("\13>\3>\3>\3>\3>\7>\u021d\n>\f>\16>\u0220\13>\5>\u0222")
        buf.write("\n>\3?\3?\3@\3@\3@\3A\3A\3A\3B\3B\3C\3C\3C\3D\3D\3E\3")
        buf.write("E\3E\3E\3E\3E\3E\3F\3F\3F\3F\3F\3F\3G\3G\3G\3G\3G\3H\3")
        buf.write("H\3H\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\3J\3J\3J\3J\3")
        buf.write("J\3K\3K\3K\3K\3K\3L\3L\3L\3L\3L\3L\3L\3M\3M\3M\3M\3N\3")
        buf.write("N\3O\3O\3O\3O\3O\3O\3P\3P\3P\3P\3P\3P\3Q\3Q\3Q\3Q\3Q\3")
        buf.write("Q\3Q\3R\3R\3R\3R\3S\3S\3S\3S\3S\3T\3T\3T\3T\3T\3U\3U\3")
        buf.write("U\3U\3V\3V\3V\3V\3V\3V\3W\3W\3W\3W\3W\3W\3W\3W\3X\3X\3")
        buf.write("X\3X\3X\3X\3X\3X\3X\3X\3Y\3Y\3Y\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3")
        buf.write("Z\3[\3[\3[\3[\3[\3[\3[\3[\3[\3[\3[\3\\\3\\\3\\\3\\\3\\")
        buf.write("\3]\3]\3]\3]\3^\3^\3^\3_\3_\3_\3_\3_\3`\3`\3`\3`\3`\3")
        buf.write("a\3a\3b\3b\3b\3b\3b\3b\3c\3c\3c\3c\3c\3c\3c\3d\3d\3d\3")
        buf.write("d\3e\3e\3e\3e\3e\3e\3e\3e\3f\3f\3f\3f\3f\3f\3f\3g\3g\3")
        buf.write("g\3g\3g\3g\3h\3h\3i\3i\3i\3i\3i\3i\3j\3j\3j\3k\3k\3k\3")
        buf.write("k\3k\3l\3l\3m\3m\3m\3m\3m\3n\3n\3n\3n\3n\3n\3n\3n\3n\3")
        buf.write("n\3n\3o\3o\3o\3o\3o\3o\3o\3o\3o\5o\u0327\no\3p\3p\3p\3")
        buf.write("p\3p\3p\3p\3p\3q\6q\u0332\nq\rq\16q\u0333\3q\3q\3q\3q")
        buf.write("\6q\u033a\nq\rq\16q\u033b\3q\3q\3q\3q\6q\u0342\nq\rq\16")
        buf.write("q\u0343\3q\3q\3q\3q\6q\u034a\nq\rq\16q\u034b\5q\u034e")
        buf.write("\nq\3r\3r\7r\u0352\nr\fr\16r\u0355\13r\3s\3s\3s\5s\u035a")
        buf.write("\ns\3t\3t\3t\3t\7t\u0360\nt\ft\16t\u0363\13t\3t\3t\3u")
        buf.write("\3u\3u\3u\6u\u036b\nu\ru\16u\u036c\3v\3v\3w\3w\3w\3x\3")
        buf.write("x\3x\3y\3y\3y\3z\3z\3z\3{\3{\3{\3|\3|\3|\3}\3}\3~\3~\5")
        buf.write("~\u0387\n~\3\177\3\177\3\177\7\177\u038c\n\177\f\177\16")
        buf.write("\177\u038f\13\177\3\177\3\177\3\177\3\177\7\177\u0395")
        buf.write("\n\177\f\177\16\177\u0398\13\177\3\177\5\177\u039b\n\177")
        buf.write("\3\u0080\3\u0080\3\u0080\3\u0080\3\u0080\7\u0080\u03a2")
        buf.write("\n\u0080\f\u0080\16\u0080\u03a5\13\u0080\3\u0080\3\u0080")
        buf.write("\3\u0080\3\u0080\3\u0080\3\u0080\3\u0080\3\u0080\7\u0080")
        buf.write("\u03af\n\u0080\f\u0080\16\u0080\u03b2\13\u0080\3\u0080")
        buf.write("\3\u0080\3\u0080\5\u0080\u03b7\n\u0080\3\u0081\3\u0081")
        buf.write("\5\u0081\u03bb\n\u0081\3\u0082\3\u0082\3\u0083\3\u0083")
        buf.write("\3\u0083\3\u0083\5\u0083\u03c3\n\u0083\5\u0215\u03a3\u03b0")
        buf.write("\2\u0084\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f")
        buf.write("\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27")
        buf.write("-\30/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%")
        buf.write("I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67")
        buf.write("m8o9q:s;u<w=y>{\2}?\177@\u0081A\u0083B\u0085C\u0087D\u0089")
        buf.write("E\u008bF\u008dG\u008fH\u0091I\u0093J\u0095K\u0097L\u0099")
        buf.write("M\u009bN\u009dO\u009fP\u00a1Q\u00a3R\u00a5S\u00a7T\u00a9")
        buf.write("U\u00abV\u00adW\u00afX\u00b1Y\u00b3Z\u00b5[\u00b7\\\u00b9")
        buf.write("]\u00bb^\u00bd_\u00bf`\u00c1a\u00c3b\u00c5c\u00c7d\u00c9")
        buf.write("e\u00cbf\u00cdg\u00cfh\u00d1i\u00d3j\u00d5k\u00d7l\u00d9")
        buf.write("m\u00dbn\u00ddo\u00dfp\u00e1q\u00e3r\u00e5s\u00e7t\u00e9")
        buf.write("u\u00eb\2\u00edv\u00efw\u00f1x\u00f3y\u00f5z\u00f7{\u00f9")
        buf.write("|\u00fb}\u00fd\2\u00ff\2\u0101\2\u0103\2\u0105\2\3\2\r")
        buf.write("\4\2\f\f\16\17\3\2\62;\5\2\62;CHch\3\2\62\63\3\2\629\5")
        buf.write("\2C\\aac|\6\2\62;C\\aac|\3\2\60\60\6\2\f\f\16\17))^^\6")
        buf.write("\2\f\f\16\17$$^^\3\2^^\2\u03df\2\3\3\2\2\2\2\5\3\2\2\2")
        buf.write("\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17")
        buf.write("\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3")
        buf.write("\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2")
        buf.write("\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3")
        buf.write("\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2")
        buf.write("\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3")
        buf.write("\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E")
        buf.write("\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2")
        buf.write("O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2")
        buf.write("\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2")
        buf.write("\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2")
        buf.write("\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2u\3")
        buf.write("\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2")
        buf.write("\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085\3\2\2\2\2\u0087")
        buf.write("\3\2\2\2\2\u0089\3\2\2\2\2\u008b\3\2\2\2\2\u008d\3\2\2")
        buf.write("\2\2\u008f\3\2\2\2\2\u0091\3\2\2\2\2\u0093\3\2\2\2\2\u0095")
        buf.write("\3\2\2\2\2\u0097\3\2\2\2\2\u0099\3\2\2\2\2\u009b\3\2\2")
        buf.write("\2\2\u009d\3\2\2\2\2\u009f\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3")
        buf.write("\3\2\2\2\2\u00a5\3\2\2\2\2\u00a7\3\2\2\2\2\u00a9\3\2\2")
        buf.write("\2\2\u00ab\3\2\2\2\2\u00ad\3\2\2\2\2\u00af\3\2\2\2\2\u00b1")
        buf.write("\3\2\2\2\2\u00b3\3\2\2\2\2\u00b5\3\2\2\2\2\u00b7\3\2\2")
        buf.write("\2\2\u00b9\3\2\2\2\2\u00bb\3\2\2\2\2\u00bd\3\2\2\2\2\u00bf")
        buf.write("\3\2\2\2\2\u00c1\3\2\2\2\2\u00c3\3\2\2\2\2\u00c5\3\2\2")
        buf.write("\2\2\u00c7\3\2\2\2\2\u00c9\3\2\2\2\2\u00cb\3\2\2\2\2\u00cd")
        buf.write("\3\2\2\2\2\u00cf\3\2\2\2\2\u00d1\3\2\2\2\2\u00d3\3\2\2")
        buf.write("\2\2\u00d5\3\2\2\2\2\u00d7\3\2\2\2\2\u00d9\3\2\2\2\2\u00db")
        buf.write("\3\2\2\2\2\u00dd\3\2\2\2\2\u00df\3\2\2\2\2\u00e1\3\2\2")
        buf.write("\2\2\u00e3\3\2\2\2\2\u00e5\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9")
        buf.write("\3\2\2\2\2\u00ed\3\2\2\2\2\u00ef\3\2\2\2\2\u00f1\3\2\2")
        buf.write("\2\2\u00f3\3\2\2\2\2\u00f5\3\2\2\2\2\u00f7\3\2\2\2\2\u00f9")
        buf.write("\3\2\2\2\2\u00fb\3\2\2\2\3\u0107\3\2\2\2\5\u010b\3\2\2")
        buf.write("\2\7\u010e\3\2\2\2\t\u0110\3\2\2\2\13\u0112\3\2\2\2\r")
        buf.write("\u0114\3\2\2\2\17\u0116\3\2\2\2\21\u0118\3\2\2\2\23\u011b")
        buf.write("\3\2\2\2\25\u011d\3\2\2\2\27\u011f\3\2\2\2\31\u0123\3")
        buf.write("\2\2\2\33\u0126\3\2\2\2\35\u0129\3\2\2\2\37\u012c\3\2")
        buf.write("\2\2!\u012f\3\2\2\2#\u0132\3\2\2\2%\u0134\3\2\2\2\'\u0137")
        buf.write("\3\2\2\2)\u0139\3\2\2\2+\u013c\3\2\2\2-\u013e\3\2\2\2")
        buf.write("/\u0140\3\2\2\2\61\u0142\3\2\2\2\63\u0146\3\2\2\2\65\u014a")
        buf.write("\3\2\2\2\67\u014e\3\2\2\29\u0156\3\2\2\2;\u015d\3\2\2")
        buf.write("\2=\u0166\3\2\2\2?\u0171\3\2\2\2A\u017d\3\2\2\2C\u0187")
        buf.write("\3\2\2\2E\u018c\3\2\2\2G\u0191\3\2\2\2I\u0195\3\2\2\2")
        buf.write("K\u0199\3\2\2\2M\u019d\3\2\2\2O\u01a1\3\2\2\2Q\u01a5\3")
        buf.write("\2\2\2S\u01a9\3\2\2\2U\u01ae\3\2\2\2W\u01b2\3\2\2\2Y\u01b7")
        buf.write("\3\2\2\2[\u01bb\3\2\2\2]\u01bf\3\2\2\2_\u01c2\3\2\2\2")
        buf.write("a\u01c5\3\2\2\2c\u01c8\3\2\2\2e\u01cb\3\2\2\2g\u01ce\3")
        buf.write("\2\2\2i\u01d1\3\2\2\2k\u01d4\3\2\2\2m\u01d8\3\2\2\2o\u01db")
        buf.write("\3\2\2\2q\u01e0\3\2\2\2s\u01e4\3\2\2\2u\u01e8\3\2\2\2")
        buf.write("w\u01ed\3\2\2\2y\u020d\3\2\2\2{\u0221\3\2\2\2}\u0223\3")
        buf.write("\2\2\2\177\u0225\3\2\2\2\u0081\u0228\3\2\2\2\u0083\u022b")
        buf.write("\3\2\2\2\u0085\u022d\3\2\2\2\u0087\u0230\3\2\2\2\u0089")
        buf.write("\u0232\3\2\2\2\u008b\u0239\3\2\2\2\u008d\u023f\3\2\2\2")
        buf.write("\u008f\u0244\3\2\2\2\u0091\u0247\3\2\2\2\u0093\u0253\3")
        buf.write("\2\2\2\u0095\u0258\3\2\2\2\u0097\u025d\3\2\2\2\u0099\u0264")
        buf.write("\3\2\2\2\u009b\u0268\3\2\2\2\u009d\u026a\3\2\2\2\u009f")
        buf.write("\u0270\3\2\2\2\u00a1\u0276\3\2\2\2\u00a3\u027d\3\2\2\2")
        buf.write("\u00a5\u0281\3\2\2\2\u00a7\u0286\3\2\2\2\u00a9\u028b\3")
        buf.write("\2\2\2\u00ab\u028f\3\2\2\2\u00ad\u0295\3\2\2\2\u00af\u029d")
        buf.write("\3\2\2\2\u00b1\u02a7\3\2\2\2\u00b3\u02aa\3\2\2\2\u00b5")
        buf.write("\u02b2\3\2\2\2\u00b7\u02bd\3\2\2\2\u00b9\u02c2\3\2\2\2")
        buf.write("\u00bb\u02c6\3\2\2\2\u00bd\u02c9\3\2\2\2\u00bf\u02ce\3")
        buf.write("\2\2\2\u00c1\u02d3\3\2\2\2\u00c3\u02d5\3\2\2\2\u00c5\u02db")
        buf.write("\3\2\2\2\u00c7\u02e2\3\2\2\2\u00c9\u02e6\3\2\2\2\u00cb")
        buf.write("\u02ee\3\2\2\2\u00cd\u02f5\3\2\2\2\u00cf\u02fb\3\2\2\2")
        buf.write("\u00d1\u02fd\3\2\2\2\u00d3\u0303\3\2\2\2\u00d5\u0306\3")
        buf.write("\2\2\2\u00d7\u030b\3\2\2\2\u00d9\u030d\3\2\2\2\u00db\u0312")
        buf.write("\3\2\2\2\u00dd\u0326\3\2\2\2\u00df\u0328\3\2\2\2\u00e1")
        buf.write("\u034d\3\2\2\2\u00e3\u034f\3\2\2\2\u00e5\u0356\3\2\2\2")
        buf.write("\u00e7\u035b\3\2\2\2\u00e9\u0366\3\2\2\2\u00eb\u036e\3")
        buf.write("\2\2\2\u00ed\u0370\3\2\2\2\u00ef\u0373\3\2\2\2\u00f1\u0376")
        buf.write("\3\2\2\2\u00f3\u0379\3\2\2\2\u00f5\u037c\3\2\2\2\u00f7")
        buf.write("\u037f\3\2\2\2\u00f9\u0382\3\2\2\2\u00fb\u0386\3\2\2\2")
        buf.write("\u00fd\u039a\3\2\2\2\u00ff\u03b6\3\2\2\2\u0101\u03ba\3")
        buf.write("\2\2\2\u0103\u03bc\3\2\2\2\u0105\u03c2\3\2\2\2\u0107\u0108")
        buf.write("\7c\2\2\u0108\u0109\7p\2\2\u0109\u010a\7f\2\2\u010a\4")
        buf.write("\3\2\2\2\u010b\u010c\7q\2\2\u010c\u010d\7t\2\2\u010d\6")
        buf.write("\3\2\2\2\u010e\u010f\7(\2\2\u010f\b\3\2\2\2\u0110\u0111")
        buf.write("\7~\2\2\u0111\n\3\2\2\2\u0112\u0113\7`\2\2\u0113\f\3\2")
        buf.write("\2\2\u0114\u0115\7/\2\2\u0115\16\3\2\2\2\u0116\u0117\7")
        buf.write("-\2\2\u0117\20\3\2\2\2\u0118\u0119\7\61\2\2\u0119\u011a")
        buf.write("\7\61\2\2\u011a\22\3\2\2\2\u011b\u011c\7\61\2\2\u011c")
        buf.write("\24\3\2\2\2\u011d\u011e\7\'\2\2\u011e\26\3\2\2\2\u011f")
        buf.write("\u0120\7o\2\2\u0120\u0121\7q\2\2\u0121\u0122\7f\2\2\u0122")
        buf.write("\30\3\2\2\2\u0123\u0124\7,\2\2\u0124\u0125\7,\2\2\u0125")
        buf.write("\32\3\2\2\2\u0126\u0127\7>\2\2\u0127\u0128\7>\2\2\u0128")
        buf.write("\34\3\2\2\2\u0129\u012a\7@\2\2\u012a\u012b\7@\2\2\u012b")
        buf.write("\36\3\2\2\2\u012c\u012d\7?\2\2\u012d\u012e\7?\2\2\u012e")
        buf.write(" \3\2\2\2\u012f\u0130\7#\2\2\u0130\u0131\7?\2\2\u0131")
        buf.write("\"\3\2\2\2\u0132\u0133\7>\2\2\u0133$\3\2\2\2\u0134\u0135")
        buf.write("\7>\2\2\u0135\u0136\7?\2\2\u0136&\3\2\2\2\u0137\u0138")
        buf.write("\7@\2\2\u0138(\3\2\2\2\u0139\u013a\7@\2\2\u013a\u013b")
        buf.write("\7?\2\2\u013b*\3\2\2\2\u013c\u013d\7\u0080\2\2\u013d,")
        buf.write("\3\2\2\2\u013e\u013f\7A\2\2\u013f.\3\2\2\2\u0140\u0141")
        buf.write("\7#\2\2\u0141\60\3\2\2\2\u0142\u0143\7c\2\2\u0143\u0144")
        buf.write("\7d\2\2\u0144\u0145\7u\2\2\u0145\62\3\2\2\2\u0146\u0147")
        buf.write("\7c\2\2\u0147\u0148\7n\2\2\u0148\u0149\7n\2\2\u0149\64")
        buf.write("\3\2\2\2\u014a\u014b\7c\2\2\u014b\u014c\7p\2\2\u014c\u014d")
        buf.write("\7{\2\2\u014d\66\3\2\2\2\u014e\u014f\7c\2\2\u014f\u0150")
        buf.write("\7v\2\2\u0150\u0151\7N\2\2\u0151\u0152\7c\2\2\u0152\u0153")
        buf.write("\7d\2\2\u0153\u0154\7g\2\2\u0154\u0155\7n\2\2\u01558\3")
        buf.write("\2\2\2\u0156\u0157\7e\2\2\u0157\u0158\7j\2\2\u0158\u0159")
        buf.write("\7q\2\2\u0159\u015a\7q\2\2\u015a\u015b\7u\2\2\u015b\u015c")
        buf.write("\7g\2\2\u015c:\3\2\2\2\u015d\u015e\7e\2\2\u015e\u015f")
        buf.write("\7q\2\2\u015f\u0160\7p\2\2\u0160\u0161\7v\2\2\u0161\u0162")
        buf.write("\7g\2\2\u0162\u0163\7z\2\2\u0163\u0164\7v\2\2\u0164\u0165")
        buf.write("\7u\2\2\u0165<\3\2\2\2\u0166\u0167\7e\2\2\u0167\u0168")
        buf.write("\7q\2\2\u0168\u0169\7w\2\2\u0169\u016a\7p\2\2\u016a\u016b")
        buf.write("\7v\2\2\u016b\u016c\7N\2\2\u016c\u016d\7c\2\2\u016d\u016e")
        buf.write("\7d\2\2\u016e\u016f\7g\2\2\u016f\u0170\7n\2\2\u0170>\3")
        buf.write("\2\2\2\u0171\u0172\7i\2\2\u0172\u0173\7g\2\2\u0173\u0174")
        buf.write("\7v\2\2\u0174\u0175\7a\2\2\u0175\u0176\7e\2\2\u0176\u0177")
        buf.write("\7q\2\2\u0177\u0178\7p\2\2\u0178\u0179\7v\2\2\u0179\u017a")
        buf.write("\7g\2\2\u017a\u017b\7z\2\2\u017b\u017c\7v\2\2\u017c@\3")
        buf.write("\2\2\2\u017d\u017e\7i\2\2\u017e\u017f\7g\2\2\u017f\u0180")
        buf.write("\7v\2\2\u0180\u0181\7a\2\2\u0181\u0182\7k\2\2\u0182\u0183")
        buf.write("\7f\2\2\u0183\u0184\7g\2\2\u0184\u0185\7p\2\2\u0185\u0186")
        buf.write("\7v\2\2\u0186B\3\2\2\2\u0187\u0188\7j\2\2\u0188\u0189")
        buf.write("\7c\2\2\u0189\u018a\7u\2\2\u018a\u018b\7j\2\2\u018bD\3")
        buf.write("\2\2\2\u018c\u018d\7m\2\2\u018d\u018e\7g\2\2\u018e\u018f")
        buf.write("\7{\2\2\u018f\u0190\7u\2\2\u0190F\3\2\2\2\u0191\u0192")
        buf.write("\7n\2\2\u0192\u0193\7g\2\2\u0193\u0194\7p\2\2\u0194H\3")
        buf.write("\2\2\2\u0195\u0196\7o\2\2\u0196\u0197\7c\2\2\u0197\u0198")
        buf.write("\7z\2\2\u0198J\3\2\2\2\u0199\u019a\7o\2\2\u019a\u019b")
        buf.write("\7k\2\2\u019b\u019c\7p\2\2\u019cL\3\2\2\2\u019d\u019e")
        buf.write("\7u\2\2\u019e\u019f\7g\2\2\u019f\u01a0\7v\2\2\u01a0N\3")
        buf.write("\2\2\2\u01a1\u01a2\7u\2\2\u01a2\u01a3\7v\2\2\u01a3\u01a4")
        buf.write("\7t\2\2\u01a4P\3\2\2\2\u01a5\u01a6\7u\2\2\u01a6\u01a7")
        buf.write("\7w\2\2\u01a7\u01a8\7o\2\2\u01a8R\3\2\2\2\u01a9\u01aa")
        buf.write("\7v\2\2\u01aa\u01ab\7{\2\2\u01ab\u01ac\7r\2\2\u01ac\u01ad")
        buf.write("\7g\2\2\u01adT\3\2\2\2\u01ae\u01af\7g\2\2\u01af\u01b0")
        buf.write("\7p\2\2\u01b0\u01b1\7f\2\2\u01b1V\3\2\2\2\u01b2\u01b3")
        buf.write("\7c\2\2\u01b3\u01b4\7p\2\2\u01b4\u01b5\7f\2\2\u01b5\u01b6")
        buf.write("\7?\2\2\u01b6X\3\2\2\2\u01b7\u01b8\7q\2\2\u01b8\u01b9")
        buf.write("\7t\2\2\u01b9\u01ba\7?\2\2\u01baZ\3\2\2\2\u01bb\u01bc")
        buf.write("\7?\2\2\u01bc\u01bd\7@\2\2\u01bd\u01be\7?\2\2\u01be\\")
        buf.write("\3\2\2\2\u01bf\u01c0\7(\2\2\u01c0\u01c1\7?\2\2\u01c1^")
        buf.write("\3\2\2\2\u01c2\u01c3\7~\2\2\u01c3\u01c4\7?\2\2\u01c4`")
        buf.write("\3\2\2\2\u01c5\u01c6\7`\2\2\u01c6\u01c7\7?\2\2\u01c7b")
        buf.write("\3\2\2\2\u01c8\u01c9\7/\2\2\u01c9\u01ca\7?\2\2\u01cad")
        buf.write("\3\2\2\2\u01cb\u01cc\7-\2\2\u01cc\u01cd\7?\2\2\u01cdf")
        buf.write("\3\2\2\2\u01ce\u01cf\7,\2\2\u01cf\u01d0\7?\2\2\u01d0h")
        buf.write("\3\2\2\2\u01d1\u01d2\7\61\2\2\u01d2\u01d3\7?\2\2\u01d3")
        buf.write("j\3\2\2\2\u01d4\u01d5\7\61\2\2\u01d5\u01d6\7\61\2\2\u01d6")
        buf.write("\u01d7\7?\2\2\u01d7l\3\2\2\2\u01d8\u01d9\7\'\2\2\u01d9")
        buf.write("\u01da\7?\2\2\u01dan\3\2\2\2\u01db\u01dc\7o\2\2\u01dc")
        buf.write("\u01dd\7q\2\2\u01dd\u01de\7f\2\2\u01de\u01df\7?\2\2\u01df")
        buf.write("p\3\2\2\2\u01e0\u01e1\7,\2\2\u01e1\u01e2\7,\2\2\u01e2")
        buf.write("\u01e3\7?\2\2\u01e3r\3\2\2\2\u01e4\u01e5\7@\2\2\u01e5")
        buf.write("\u01e6\7@\2\2\u01e6\u01e7\7?\2\2\u01e7t\3\2\2\2\u01e8")
        buf.write("\u01e9\7>\2\2\u01e9\u01ea\7>\2\2\u01ea\u01eb\7?\2\2\u01eb")
        buf.write("v\3\2\2\2\u01ec\u01ee\7\17\2\2\u01ed\u01ec\3\2\2\2\u01ed")
        buf.write("\u01ee\3\2\2\2\u01ee\u01ef\3\2\2\2\u01ef\u01fc\7\f\2\2")
        buf.write("\u01f0\u01f2\7\"\2\2\u01f1\u01f0\3\2\2\2\u01f2\u01f5\3")
        buf.write("\2\2\2\u01f3\u01f1\3\2\2\2\u01f3\u01f4\3\2\2\2\u01f4\u01fd")
        buf.write("\3\2\2\2\u01f5\u01f3\3\2\2\2\u01f6\u01f8\7\13\2\2\u01f7")
        buf.write("\u01f6\3\2\2\2\u01f8\u01fb\3\2\2\2\u01f9\u01f7\3\2\2\2")
        buf.write("\u01f9\u01fa\3\2\2\2\u01fa\u01fd\3\2\2\2\u01fb\u01f9\3")
        buf.write("\2\2\2\u01fc\u01f3\3\2\2\2\u01fc\u01f9\3\2\2\2\u01fd\u01fe")
        buf.write("\3\2\2\2\u01fe\u01ff\b<\2\2\u01ffx\3\2\2\2\u0200\u0202")
        buf.write("\7\"\2\2\u0201\u0200\3\2\2\2\u0202\u0203\3\2\2\2\u0203")
        buf.write("\u0201\3\2\2\2\u0203\u0204\3\2\2\2\u0204\u020e\3\2\2\2")
        buf.write("\u0205\u0207\7\13\2\2\u0206\u0205\3\2\2\2\u0207\u0208")
        buf.write("\3\2\2\2\u0208\u0206\3\2\2\2\u0208\u0209\3\2\2\2\u0209")
        buf.write("\u020e\3\2\2\2\u020a\u020b\7^\2\2\u020b\u020e\5w<\2\u020c")
        buf.write("\u020e\5{>\2\u020d\u0201\3\2\2\2\u020d\u0206\3\2\2\2\u020d")
        buf.write("\u020a\3\2\2\2\u020d\u020c\3\2\2\2\u020e\u020f\3\2\2\2")
        buf.write("\u020f\u0210\b=\3\2\u0210z\3\2\2\2\u0211\u0215\5\177@")
        buf.write("\2\u0212\u0214\13\2\2\2\u0213\u0212\3\2\2\2\u0214\u0217")
        buf.write("\3\2\2\2\u0215\u0216\3\2\2\2\u0215\u0213\3\2\2\2\u0216")
        buf.write("\u0218\3\2\2\2\u0217\u0215\3\2\2\2\u0218\u0219\5\u0081")
        buf.write("A\2\u0219\u0222\3\2\2\2\u021a\u021e\5}?\2\u021b\u021d")
        buf.write("\n\2\2\2\u021c\u021b\3\2\2\2\u021d\u0220\3\2\2\2\u021e")
        buf.write("\u021c\3\2\2\2\u021e\u021f\3\2\2\2\u021f\u0222\3\2\2\2")
        buf.write("\u0220\u021e\3\2\2\2\u0221\u0211\3\2\2\2\u0221\u021a\3")
        buf.write("\2\2\2\u0222|\3\2\2\2\u0223\u0224\7%\2\2\u0224~\3\2\2")
        buf.write("\2\u0225\u0226\7*\2\2\u0226\u0227\7,\2\2\u0227\u0080\3")
        buf.write("\2\2\2\u0228\u0229\7,\2\2\u0229\u022a\7+\2\2\u022a\u0082")
        buf.write("\3\2\2\2\u022b\u022c\7,\2\2\u022c\u0084\3\2\2\2\u022d")
        buf.write("\u022e\7c\2\2\u022e\u022f\7u\2\2\u022f\u0086\3\2\2\2\u0230")
        buf.write("\u0231\7\60\2\2\u0231\u0088\3\2\2\2\u0232\u0233\7k\2\2")
        buf.write("\u0233\u0234\7o\2\2\u0234\u0235\7r\2\2\u0235\u0236\7q")
        buf.write("\2\2\u0236\u0237\7t\2\2\u0237\u0238\7v\2\2\u0238\u008a")
        buf.write("\3\2\2\2\u0239\u023a\7r\2\2\u023a\u023b\7t\2\2\u023b\u023c")
        buf.write("\7k\2\2\u023c\u023d\7p\2\2\u023d\u023e\7v\2\2\u023e\u008c")
        buf.write("\3\2\2\2\u023f\u0240\7h\2\2\u0240\u0241\7t\2\2\u0241\u0242")
        buf.write("\7q\2\2\u0242\u0243\7o\2\2\u0243\u008e\3\2\2\2\u0244\u0245")
        buf.write("\7\60\2\2\u0245\u0246\7\60\2\2\u0246\u0090\3\2\2\2\u0247")
        buf.write("\u0248\7u\2\2\u0248\u0249\7g\2\2\u0249\u024a\7v\2\2\u024a")
        buf.write("\u024b\7k\2\2\u024b\u024c\7p\2\2\u024c\u024d\7v\2\2\u024d")
        buf.write("\u024e\7n\2\2\u024e\u024f\7g\2\2\u024f\u0250\7x\2\2\u0250")
        buf.write("\u0251\7g\2\2\u0251\u0252\7n\2\2\u0252\u0092\3\2\2\2\u0253")
        buf.write("\u0254\7u\2\2\u0254\u0255\7c\2\2\u0255\u0256\7x\2\2\u0256")
        buf.write("\u0257\7g\2\2\u0257\u0094\3\2\2\2\u0258\u0259\7u\2\2\u0259")
        buf.write("\u025a\7v\2\2\u025a\u025b\7q\2\2\u025b\u025c\7r\2\2\u025c")
        buf.write("\u0096\3\2\2\2\u025d\u025e\7n\2\2\u025e\u025f\7c\2\2\u025f")
        buf.write("\u0260\7o\2\2\u0260\u0261\7d\2\2\u0261\u0262\7f\2\2\u0262")
        buf.write("\u0263\7c\2\2\u0263\u0098\3\2\2\2\u0264\u0265\7p\2\2\u0265")
        buf.write("\u0266\7q\2\2\u0266\u0267\7v\2\2\u0267\u009a\3\2\2\2\u0268")
        buf.write("\u0269\7.\2\2\u0269\u009c\3\2\2\2\u026a\u026b\7e\2\2\u026b")
        buf.write("\u026c\7q\2\2\u026c\u026d\7p\2\2\u026d\u026e\7u\2\2\u026e")
        buf.write("\u026f\7v\2\2\u026f\u009e\3\2\2\2\u0270\u0271\7c\2\2\u0271")
        buf.write("\u0272\7y\2\2\u0272\u0273\7c\2\2\u0273\u0274\7k\2\2\u0274")
        buf.write("\u0275\7v\2\2\u0275\u00a0\3\2\2\2\u0276\u0277\7c\2\2\u0277")
        buf.write("\u0278\7u\2\2\u0278\u0279\7u\2\2\u0279\u027a\7g\2\2\u027a")
        buf.write("\u027b\7t\2\2\u027b\u027c\7v\2\2\u027c\u00a2\3\2\2\2\u027d")
        buf.write("\u027e\7x\2\2\u027e\u027f\7c\2\2\u027f\u0280\7t\2\2\u0280")
        buf.write("\u00a4\3\2\2\2\u0281\u0282\7v\2\2\u0282\u0283\7t\2\2\u0283")
        buf.write("\u0284\7c\2\2\u0284\u0285\7r\2\2\u0285\u00a6\3\2\2\2\u0286")
        buf.write("\u0287\7r\2\2\u0287\u0288\7c\2\2\u0288\u0289\7u\2\2\u0289")
        buf.write("\u028a\7u\2\2\u028a\u00a8\3\2\2\2\u028b\u028c\7f\2\2\u028c")
        buf.write("\u028d\7g\2\2\u028d\u028e\7n\2\2\u028e\u00aa\3\2\2\2\u028f")
        buf.write("\u0290\7u\2\2\u0290\u0291\7r\2\2\u0291\u0292\7c\2\2\u0292")
        buf.write("\u0293\7y\2\2\u0293\u0294\7p\2\2\u0294\u00ac\3\2\2\2\u0295")
        buf.write("\u0296\7h\2\2\u0296\u0297\7k\2\2\u0297\u0298\7p\2\2\u0298")
        buf.write("\u0299\7c\2\2\u0299\u029a\7n\2\2\u029a\u029b\7n\2\2\u029b")
        buf.write("\u029c\7{\2\2\u029c\u00ae\3\2\2\2\u029d\u029e\7k\2\2\u029e")
        buf.write("\u029f\7p\2\2\u029f\u02a0\7x\2\2\u02a0\u02a1\7c\2\2\u02a1")
        buf.write("\u02a2\7t\2\2\u02a2\u02a3\7k\2\2\u02a3\u02a4\7c\2\2\u02a4")
        buf.write("\u02a5\7p\2\2\u02a5\u02a6\7v\2\2\u02a6\u00b0\3\2\2\2\u02a7")
        buf.write("\u02a8\7i\2\2\u02a8\u02a9\7q\2\2\u02a9\u00b2\3\2\2\2\u02aa")
        buf.write("\u02ab\7d\2\2\u02ab\u02ac\7w\2\2\u02ac\u02ad\7k\2\2\u02ad")
        buf.write("\u02ae\7n\2\2\u02ae\u02af\7v\2\2\u02af\u02b0\7k\2\2\u02b0")
        buf.write("\u02b1\7p\2\2\u02b1\u00b4\3\2\2\2\u02b2\u02b3\7u\2\2\u02b3")
        buf.write("\u02b4\7g\2\2\u02b4\u02b5\7s\2\2\u02b5\u02b6\7w\2\2\u02b6")
        buf.write("\u02b7\7g\2\2\u02b7\u02b8\7p\2\2\u02b8\u02b9\7v\2\2\u02b9")
        buf.write("\u02ba\7k\2\2\u02ba\u02bb\7c\2\2\u02bb\u02bc\7n\2\2\u02bc")
        buf.write("\u00b6\3\2\2\2\u02bd\u02be\7y\2\2\u02be\u02bf\7j\2\2\u02bf")
        buf.write("\u02c0\7g\2\2\u02c0\u02c1\7p\2\2\u02c1\u00b8\3\2\2\2\u02c2")
        buf.write("\u02c3\7n\2\2\u02c3\u02c4\7g\2\2\u02c4\u02c5\7v\2\2\u02c5")
        buf.write("\u00ba\3\2\2\2\u02c6\u02c7\7k\2\2\u02c7\u02c8\7h\2\2\u02c8")
        buf.write("\u00bc\3\2\2\2\u02c9\u02ca\7g\2\2\u02ca\u02cb\7n\2\2\u02cb")
        buf.write("\u02cc\7k\2\2\u02cc\u02cd\7h\2\2\u02cd\u00be\3\2\2\2\u02ce")
        buf.write("\u02cf\7g\2\2\u02cf\u02d0\7n\2\2\u02d0\u02d1\7u\2\2\u02d1")
        buf.write("\u02d2\7g\2\2\u02d2\u00c0\3\2\2\2\u02d3\u02d4\7B\2\2\u02d4")
        buf.write("\u00c2\3\2\2\2\u02d5\u02d6\7y\2\2\u02d6\u02d7\7j\2\2\u02d7")
        buf.write("\u02d8\7k\2\2\u02d8\u02d9\7n\2\2\u02d9\u02da\7g\2\2\u02da")
        buf.write("\u00c4\3\2\2\2\u02db\u02dc\7i\2\2\u02dc\u02dd\7n\2\2\u02dd")
        buf.write("\u02de\7q\2\2\u02de\u02df\7d\2\2\u02df\u02e0\7c\2\2\u02e0")
        buf.write("\u02e1\7n\2\2\u02e1\u00c6\3\2\2\2\u02e2\u02e3\7f\2\2\u02e3")
        buf.write("\u02e4\7g\2\2\u02e4\u02e5\7h\2\2\u02e5\u00c8\3\2\2\2\u02e6")
        buf.write("\u02e7\7t\2\2\u02e7\u02e8\7g\2\2\u02e8\u02e9\7v\2\2\u02e9")
        buf.write("\u02ea\7w\2\2\u02ea\u02eb\7t\2\2\u02eb\u02ec\7p\2\2\u02ec")
        buf.write("\u02ed\7u\2\2\u02ed\u00ca\3\2\2\2\u02ee\u02ef\7g\2\2\u02ef")
        buf.write("\u02f0\7z\2\2\u02f0\u02f1\7k\2\2\u02f1\u02f2\7u\2\2\u02f2")
        buf.write("\u02f3\7v\2\2\u02f3\u02f4\7u\2\2\u02f4\u00cc\3\2\2\2\u02f5")
        buf.write("\u02f6\7y\2\2\u02f6\u02f7\7j\2\2\u02f7\u02f8\7g\2\2\u02f8")
        buf.write("\u02f9\7t\2\2\u02f9\u02fa\7g\2\2\u02fa\u00ce\3\2\2\2\u02fb")
        buf.write("\u02fc\7?\2\2\u02fc\u00d0\3\2\2\2\u02fd\u02fe\7h\2\2\u02fe")
        buf.write("\u02ff\7q\2\2\u02ff\u0300\7t\2\2\u0300\u0301\3\2\2\2\u0301")
        buf.write("\u0302\bi\4\2\u0302\u00d2\3\2\2\2\u0303\u0304\7?\2\2\u0304")
        buf.write("\u0305\7@\2\2\u0305\u00d4\3\2\2\2\u0306\u0307\7k\2\2\u0307")
        buf.write("\u0308\7p\2\2\u0308\u0309\3\2\2\2\u0309\u030a\bk\5\2\u030a")
        buf.write("\u00d6\3\2\2\2\u030b\u030c\7<\2\2\u030c\u00d8\3\2\2\2")
        buf.write("\u030d\u030e\7P\2\2\u030e\u030f\7q\2\2\u030f\u0310\7p")
        buf.write("\2\2\u0310\u0311\7g\2\2\u0311\u00da\3\2\2\2\u0312\u0313")
        buf.write("\7c\2\2\u0313\u0314\7v\2\2\u0314\u0315\7q\2\2\u0315\u0316")
        buf.write("\7o\2\2\u0316\u0317\7k\2\2\u0317\u0318\7e\2\2\u0318\u0319")
        buf.write("\7c\2\2\u0319\u031a\7n\2\2\u031a\u031b\7n\2\2\u031b\u031c")
        buf.write("\7{\2\2\u031c\u00dc\3\2\2\2\u031d\u031e\7H\2\2\u031e\u031f")
        buf.write("\7c\2\2\u031f\u0320\7n\2\2\u0320\u0321\7u\2\2\u0321\u0327")
        buf.write("\7g\2\2\u0322\u0323\7V\2\2\u0323\u0324\7t\2\2\u0324\u0325")
        buf.write("\7w\2\2\u0325\u0327\7g\2\2\u0326\u031d\3\2\2\2\u0326\u0322")
        buf.write("\3\2\2\2\u0327\u00de\3\2\2\2\u0328\u0329\7g\2\2\u0329")
        buf.write("\u032a\7v\2\2\u032a\u032b\7g\2\2\u032b\u032c\7t\2\2\u032c")
        buf.write("\u032d\7p\2\2\u032d\u032e\7c\2\2\u032e\u032f\7n\2\2\u032f")
        buf.write("\u00e0\3\2\2\2\u0330\u0332\t\3\2\2\u0331\u0330\3\2\2\2")
        buf.write("\u0332\u0333\3\2\2\2\u0333\u0331\3\2\2\2\u0333\u0334\3")
        buf.write("\2\2\2\u0334\u034e\3\2\2\2\u0335\u0336\7\62\2\2\u0336")
        buf.write("\u0337\7z\2\2\u0337\u0339\3\2\2\2\u0338\u033a\t\4\2\2")
        buf.write("\u0339\u0338\3\2\2\2\u033a\u033b\3\2\2\2\u033b\u0339\3")
        buf.write("\2\2\2\u033b\u033c\3\2\2\2\u033c\u034e\3\2\2\2\u033d\u033e")
        buf.write("\7\62\2\2\u033e\u033f\7d\2\2\u033f\u0341\3\2\2\2\u0340")
        buf.write("\u0342\t\5\2\2\u0341\u0340\3\2\2\2\u0342\u0343\3\2\2\2")
        buf.write("\u0343\u0341\3\2\2\2\u0343\u0344\3\2\2\2\u0344\u034e\3")
        buf.write("\2\2\2\u0345\u0346\7\62\2\2\u0346\u0347\7q\2\2\u0347\u0349")
        buf.write("\3\2\2\2\u0348\u034a\t\6\2\2\u0349\u0348\3\2\2\2\u034a")
        buf.write("\u034b\3\2\2\2\u034b\u0349\3\2\2\2\u034b\u034c\3\2\2\2")
        buf.write("\u034c\u034e\3\2\2\2\u034d\u0331\3\2\2\2\u034d\u0335\3")
        buf.write("\2\2\2\u034d\u033d\3\2\2\2\u034d\u0345\3\2\2\2\u034e\u00e2")
        buf.write("\3\2\2\2\u034f\u0353\t\7\2\2\u0350\u0352\t\b\2\2\u0351")
        buf.write("\u0350\3\2\2\2\u0352\u0355\3\2\2\2\u0353\u0351\3\2\2\2")
        buf.write("\u0353\u0354\3\2\2\2\u0354\u00e4\3\2\2\2\u0355\u0353\3")
        buf.write("\2\2\2\u0356\u0359\t\t\2\2\u0357\u035a\5\u00e9u\2\u0358")
        buf.write("\u035a\5\u00e3r\2\u0359\u0357\3\2\2\2\u0359\u0358\3\2")
        buf.write("\2\2\u035a\u00e6\3\2\2\2\u035b\u035c\7/\2\2\u035c\u035d")
        buf.write("\7@\2\2\u035d\u0361\3\2\2\2\u035e\u0360\7\"\2\2\u035f")
        buf.write("\u035e\3\2\2\2\u0360\u0363\3\2\2\2\u0361\u035f\3\2\2\2")
        buf.write("\u0361\u0362\3\2\2\2\u0362\u0364\3\2\2\2\u0363\u0361\3")
        buf.write("\2\2\2\u0364\u0365\5\u00e3r\2\u0365\u00e8\3\2\2\2\u0366")
        buf.write("\u0367\7\62\2\2\u0367\u0368\7Z\2\2\u0368\u036a\3\2\2\2")
        buf.write("\u0369\u036b\5\u00ebv\2\u036a\u0369\3\2\2\2\u036b\u036c")
        buf.write("\3\2\2\2\u036c\u036a\3\2\2\2\u036c\u036d\3\2\2\2\u036d")
        buf.write("\u00ea\3\2\2\2\u036e\u036f\t\4\2\2\u036f\u00ec\3\2\2\2")
        buf.write("\u0370\u0371\7]\2\2\u0371\u0372\bw\6\2\u0372\u00ee\3\2")
        buf.write("\2\2\u0373\u0374\7_\2\2\u0374\u0375\bx\7\2\u0375\u00f0")
        buf.write("\3\2\2\2\u0376\u0377\7}\2\2\u0377\u0378\by\b\2\u0378\u00f2")
        buf.write("\3\2\2\2\u0379\u037a\7\177\2\2\u037a\u037b\bz\t\2\u037b")
        buf.write("\u00f4\3\2\2\2\u037c\u037d\7*\2\2\u037d\u037e\b{\n\2\u037e")
        buf.write("\u00f6\3\2\2\2\u037f\u0380\7+\2\2\u0380\u0381\b|\13\2")
        buf.write("\u0381\u00f8\3\2\2\2\u0382\u0383\7=\2\2\u0383\u00fa\3")
        buf.write("\2\2\2\u0384\u0387\5\u00fd\177\2\u0385\u0387\5\u00ff\u0080")
        buf.write("\2\u0386\u0384\3\2\2\2\u0386\u0385\3\2\2\2\u0387\u00fc")
        buf.write("\3\2\2\2\u0388\u038d\7)\2\2\u0389\u038c\5\u0105\u0083")
        buf.write("\2\u038a\u038c\n\n\2\2\u038b\u0389\3\2\2\2\u038b\u038a")
        buf.write("\3\2\2\2\u038c\u038f\3\2\2\2\u038d\u038b\3\2\2\2\u038d")
        buf.write("\u038e\3\2\2\2\u038e\u0390\3\2\2\2\u038f\u038d\3\2\2\2")
        buf.write("\u0390\u039b\7)\2\2\u0391\u0396\7$\2\2\u0392\u0395\5\u0105")
        buf.write("\u0083\2\u0393\u0395\n\13\2\2\u0394\u0392\3\2\2\2\u0394")
        buf.write("\u0393\3\2\2\2\u0395\u0398\3\2\2\2\u0396\u0394\3\2\2\2")
        buf.write("\u0396\u0397\3\2\2\2\u0397\u0399\3\2\2\2\u0398\u0396\3")
        buf.write("\2\2\2\u0399\u039b\7$\2\2\u039a\u0388\3\2\2\2\u039a\u0391")
        buf.write("\3\2\2\2\u039b\u00fe\3\2\2\2\u039c\u039d\7)\2\2\u039d")
        buf.write("\u039e\7)\2\2\u039e\u039f\7)\2\2\u039f\u03a3\3\2\2\2\u03a0")
        buf.write("\u03a2\5\u0101\u0081\2\u03a1\u03a0\3\2\2\2\u03a2\u03a5")
        buf.write("\3\2\2\2\u03a3\u03a4\3\2\2\2\u03a3\u03a1\3\2\2\2\u03a4")
        buf.write("\u03a6\3\2\2\2\u03a5\u03a3\3\2\2\2\u03a6\u03a7\7)\2\2")
        buf.write("\u03a7\u03a8\7)\2\2\u03a8\u03b7\7)\2\2\u03a9\u03aa\7$")
        buf.write("\2\2\u03aa\u03ab\7$\2\2\u03ab\u03ac\7$\2\2\u03ac\u03b0")
        buf.write("\3\2\2\2\u03ad\u03af\5\u0101\u0081\2\u03ae\u03ad\3\2\2")
        buf.write("\2\u03af\u03b2\3\2\2\2\u03b0\u03b1\3\2\2\2\u03b0\u03ae")
        buf.write("\3\2\2\2\u03b1\u03b3\3\2\2\2\u03b2\u03b0\3\2\2\2\u03b3")
        buf.write("\u03b4\7$\2\2\u03b4\u03b5\7$\2\2\u03b5\u03b7\7$\2\2\u03b6")
        buf.write("\u039c\3\2\2\2\u03b6\u03a9\3\2\2\2\u03b7\u0100\3\2\2\2")
        buf.write("\u03b8\u03bb\5\u0103\u0082\2\u03b9\u03bb\5\u0105\u0083")
        buf.write("\2\u03ba\u03b8\3\2\2\2\u03ba\u03b9\3\2\2\2\u03bb\u0102")
        buf.write("\3\2\2\2\u03bc\u03bd\n\f\2\2\u03bd\u0104\3\2\2\2\u03be")
        buf.write("\u03bf\7^\2\2\u03bf\u03c3\13\2\2\2\u03c0\u03c1\7^\2\2")
        buf.write("\u03c1\u03c3\5w<\2\u03c2\u03be\3\2\2\2\u03c2\u03c0\3\2")
        buf.write("\2\2\u03c3\u0106\3\2\2\2\"\2\u01ed\u01f3\u01f9\u01fc\u0203")
        buf.write("\u0208\u020d\u0215\u021e\u0221\u0326\u0333\u033b\u0343")
        buf.write("\u034b\u034d\u0353\u0359\u0361\u036c\u0386\u038b\u038d")
        buf.write("\u0394\u0396\u039a\u03a3\u03b0\u03b6\u03ba\u03c2\f\3<")
        buf.write("\2\b\2\2\3i\3\3k\4\3w\5\3x\6\3y\7\3z\b\3{\t\3|\n")
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
    NL = 59
    WS = 60
    COMMENT_START = 61
    OPEN_MULTI_COMMENT = 62
    CLOSE_MULTI_COMMENT = 63
    STAR = 64
    AS = 65
    DOT = 66
    IMPORT = 67
    PRINT = 68
    FROM = 69
    RANGE = 70
    SETINTLEVEL = 71
    SAVE = 72
    STOP = 73
    LAMBDA = 74
    NOT = 75
    COMMA = 76
    CONST = 77
    AWAIT = 78
    ASSERT = 79
    VAR = 80
    TRAP = 81
    PASS = 82
    DEL = 83
    SPAWN = 84
    FINALLY = 85
    INVARIANT = 86
    GO = 87
    BUILTIN = 88
    SEQUENTIAL = 89
    WHEN = 90
    LET = 91
    IF = 92
    ELIF = 93
    ELSE = 94
    AT = 95
    WHILE = 96
    GLOBAL = 97
    DEF = 98
    RETURNS = 99
    EXISTS = 100
    WHERE = 101
    EQ = 102
    FOR = 103
    IMPLIES = 104
    IN = 105
    COLON = 106
    NONE = 107
    ATOMICALLY = 108
    BOOL = 109
    ETERNAL = 110
    INT = 111
    NAME = 112
    ATOM = 113
    ARROWID = 114
    HEX_INTEGER = 115
    OPEN_BRACK = 116
    CLOSE_BRACK = 117
    OPEN_BRACES = 118
    CLOSE_BRACES = 119
    OPEN_PAREN = 120
    CLOSE_PAREN = 121
    SEMI_COLON = 122
    STRING = 123

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'or'", "'&'", "'|'", "'^'", "'-'", "'+'", "'//'", 
            "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", "'!='", 
            "'<'", "'<='", "'>'", "'>='", "'~'", "'?'", "'!'", "'abs'", 
            "'all'", "'any'", "'atLabel'", "'choose'", "'contexts'", "'countLabel'", 
            "'get_context'", "'get_ident'", "'hash'", "'keys'", "'len'", 
            "'max'", "'min'", "'set'", "'str'", "'sum'", "'type'", "'end'", 
            "'and='", "'or='", "'=>='", "'&='", "'|='", "'^='", "'-='", 
            "'+='", "'*='", "'/='", "'//='", "'%='", "'mod='", "'**='", 
            "'>>='", "'<<='", "'#'", "'(*'", "'*)'", "'*'", "'as'", "'.'", 
            "'import'", "'print'", "'from'", "'..'", "'setintlevel'", "'save'", 
            "'stop'", "'lambda'", "'not'", "','", "'const'", "'await'", 
            "'assert'", "'var'", "'trap'", "'pass'", "'del'", "'spawn'", 
            "'finally'", "'invariant'", "'go'", "'builtin'", "'sequential'", 
            "'when'", "'let'", "'if'", "'elif'", "'else'", "'@'", "'while'", 
            "'global'", "'def'", "'returns'", "'exists'", "'where'", "'='", 
            "'for'", "'=>'", "'in'", "':'", "'None'", "'atomically'", "'eternal'", 
            "'['", "']'", "'{'", "'}'", "'('", "')'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "NL", "WS", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
            "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", "RANGE", "SETINTLEVEL", 
            "SAVE", "STOP", "LAMBDA", "NOT", "COMMA", "CONST", "AWAIT", 
            "ASSERT", "VAR", "TRAP", "PASS", "DEL", "SPAWN", "FINALLY", 
            "INVARIANT", "GO", "BUILTIN", "SEQUENTIAL", "WHEN", "LET", "IF", 
            "ELIF", "ELSE", "AT", "WHILE", "GLOBAL", "DEF", "RETURNS", "EXISTS", 
            "WHERE", "EQ", "FOR", "IMPLIES", "IN", "COLON", "NONE", "ATOMICALLY", 
            "BOOL", "ETERNAL", "INT", "NAME", "ATOM", "ARROWID", "HEX_INTEGER", 
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
                  "T__56", "T__57", "NL", "WS", "COMMENT", "COMMENT_START", 
                  "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", "STAR", "AS", 
                  "DOT", "IMPORT", "PRINT", "FROM", "RANGE", "SETINTLEVEL", 
                  "SAVE", "STOP", "LAMBDA", "NOT", "COMMA", "CONST", "AWAIT", 
                  "ASSERT", "VAR", "TRAP", "PASS", "DEL", "SPAWN", "FINALLY", 
                  "INVARIANT", "GO", "BUILTIN", "SEQUENTIAL", "WHEN", "LET", 
                  "IF", "ELIF", "ELSE", "AT", "WHILE", "GLOBAL", "DEF", 
                  "RETURNS", "EXISTS", "WHERE", "EQ", "FOR", "IMPLIES", 
                  "IN", "COLON", "NONE", "ATOMICALLY", "BOOL", "ETERNAL", 
                  "INT", "NAME", "ATOM", "ARROWID", "HEX_INTEGER", "HEX_DIGIT", 
                  "OPEN_BRACK", "CLOSE_BRACK", "OPEN_BRACES", "CLOSE_BRACES", 
                  "OPEN_PAREN", "CLOSE_PAREN", "SEMI_COLON", "STRING", "SHORT_STRING", 
                  "LONG_STRING", "LONG_STRING_ITEM", "LONG_STRING_CHAR", 
                  "STRING_ESCAPE_SEQ" ]

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
            actions[58] = self.NL_action 
            actions[103] = self.FOR_action 
            actions[105] = self.IN_action 
            actions[117] = self.OPEN_BRACK_action 
            actions[118] = self.CLOSE_BRACK_action 
            actions[119] = self.OPEN_BRACES_action 
            actions[120] = self.CLOSE_BRACES_action 
            actions[121] = self.OPEN_PAREN_action 
            actions[122] = self.CLOSE_PAREN_action 
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
     


