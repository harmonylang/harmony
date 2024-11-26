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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\177")
        buf.write("\u03d0\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("\4\u0084\t\u0084\4\u0085\t\u0085\3\2\3\2\3\2\3\2\3\3\3")
        buf.write("\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t")
        buf.write("\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\16")
        buf.write("\3\16\3\16\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\22\3\22\3\23\3\23\3\23\3\24\3\24\3\25\3\25\3\25\3\26")
        buf.write("\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3\31\3\31\3\32\3\32")
        buf.write("\3\32\3\32\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37")
        buf.write("\3\37\3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3!\3!\3!\3!\3!")
        buf.write("\3!\3!\3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"")
        buf.write("\3\"\3\"\3#\3#\3#\3#\3#\3$\3$\3$\3$\3%\3%\3%\3%\3%\3&")
        buf.write("\3&\3&\3&\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3)\3)\3)\3)\3*\3")
        buf.write("*\3*\3*\3+\3+\3+\3+\3,\3,\3,\3,\3,\3-\3-\3-\3-\3.\3.\3")
        buf.write(".\3.\3.\3/\3/\3/\3/\3\60\3\60\3\60\3\60\3\61\3\61\3\61")
        buf.write("\3\62\3\62\3\62\3\63\3\63\3\63\3\64\3\64\3\64\3\65\3\65")
        buf.write("\3\65\3\66\3\66\3\66\3\67\3\67\3\67\38\38\38\38\39\39")
        buf.write("\39\3:\3:\3:\3:\3:\3;\3;\3;\3;\3<\3<\3<\3<\3=\3=\3=\3")
        buf.write("=\3>\5>\u01fa\n>\3>\3>\7>\u01fe\n>\f>\16>\u0201\13>\3")
        buf.write(">\7>\u0204\n>\f>\16>\u0207\13>\5>\u0209\n>\3>\3>\3?\6")
        buf.write("?\u020e\n?\r?\16?\u020f\3?\6?\u0213\n?\r?\16?\u0214\3")
        buf.write("?\3?\3?\5?\u021a\n?\3?\3?\3@\3@\7@\u0220\n@\f@\16@\u0223")
        buf.write("\13@\3@\3@\3@\3@\7@\u0229\n@\f@\16@\u022c\13@\5@\u022e")
        buf.write("\n@\3A\3A\3B\3B\3B\3C\3C\3C\3D\3D\3E\3E\3E\3F\3F\3G\3")
        buf.write("G\3G\3G\3G\3G\3G\3H\3H\3H\3H\3H\3H\3I\3I\3I\3I\3I\3J\3")
        buf.write("J\3J\3K\3K\3K\3K\3K\3K\3K\3K\3K\3K\3K\3K\3L\3L\3L\3L\3")
        buf.write("L\3M\3M\3M\3M\3M\3N\3N\3N\3N\3N\3N\3N\3O\3O\3O\3O\3P\3")
        buf.write("P\3Q\3Q\3Q\3Q\3Q\3Q\3R\3R\3R\3R\3R\3R\3S\3S\3S\3S\3S\3")
        buf.write("S\3S\3T\3T\3T\3T\3U\3U\3U\3U\3U\3V\3V\3V\3V\3V\3W\3W\3")
        buf.write("W\3W\3X\3X\3X\3X\3X\3X\3Y\3Y\3Y\3Y\3Y\3Y\3Y\3Y\3Z\3Z\3")
        buf.write("Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3[\3[\3[\3\\\3\\\3\\\3\\\3\\\3")
        buf.write("\\\3\\\3\\\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3^\3^\3^\3")
        buf.write("^\3^\3_\3_\3_\3_\3`\3`\3`\3a\3a\3a\3a\3a\3b\3b\3b\3b\3")
        buf.write("b\3c\3c\3d\3d\3d\3d\3d\3d\3e\3e\3e\3e\3e\3e\3e\3f\3f\3")
        buf.write("f\3f\3g\3g\3g\3g\3g\3g\3g\3g\3h\3h\3h\3h\3h\3h\3h\3i\3")
        buf.write("i\3i\3i\3i\3i\3j\3j\3k\3k\3k\3k\3k\3k\3l\3l\3l\3m\3m\3")
        buf.write("m\3m\3m\3n\3n\3o\3o\3o\3o\3o\3p\3p\3p\3p\3p\3p\3p\3p\3")
        buf.write("p\3p\3p\3q\3q\3q\3q\3q\3q\3q\3q\3q\5q\u0333\nq\3r\3r\3")
        buf.write("r\3r\3r\3r\3r\3r\3s\6s\u033e\ns\rs\16s\u033f\3s\3s\3s")
        buf.write("\3s\6s\u0346\ns\rs\16s\u0347\3s\3s\3s\3s\6s\u034e\ns\r")
        buf.write("s\16s\u034f\3s\3s\3s\3s\6s\u0356\ns\rs\16s\u0357\5s\u035a")
        buf.write("\ns\3t\3t\7t\u035e\nt\ft\16t\u0361\13t\3u\3u\3u\5u\u0366")
        buf.write("\nu\3v\3v\3v\3v\7v\u036c\nv\fv\16v\u036f\13v\3v\3v\3w")
        buf.write("\3w\3w\3w\6w\u0377\nw\rw\16w\u0378\3x\3x\3y\3y\3y\3z\3")
        buf.write("z\3z\3{\3{\3{\3|\3|\3|\3}\3}\3}\3~\3~\3~\3\177\3\177\3")
        buf.write("\u0080\3\u0080\5\u0080\u0393\n\u0080\3\u0081\3\u0081\3")
        buf.write("\u0081\7\u0081\u0398\n\u0081\f\u0081\16\u0081\u039b\13")
        buf.write("\u0081\3\u0081\3\u0081\3\u0081\3\u0081\7\u0081\u03a1\n")
        buf.write("\u0081\f\u0081\16\u0081\u03a4\13\u0081\3\u0081\5\u0081")
        buf.write("\u03a7\n\u0081\3\u0082\3\u0082\3\u0082\3\u0082\3\u0082")
        buf.write("\7\u0082\u03ae\n\u0082\f\u0082\16\u0082\u03b1\13\u0082")
        buf.write("\3\u0082\3\u0082\3\u0082\3\u0082\3\u0082\3\u0082\3\u0082")
        buf.write("\3\u0082\7\u0082\u03bb\n\u0082\f\u0082\16\u0082\u03be")
        buf.write("\13\u0082\3\u0082\3\u0082\3\u0082\5\u0082\u03c3\n\u0082")
        buf.write("\3\u0083\3\u0083\5\u0083\u03c7\n\u0083\3\u0084\3\u0084")
        buf.write("\3\u0085\3\u0085\3\u0085\3\u0085\5\u0085\u03cf\n\u0085")
        buf.write("\5\u0221\u03af\u03bc\2\u0086\3\3\5\4\7\5\t\6\13\7\r\b")
        buf.write("\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22")
        buf.write("#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67\35")
        buf.write("9\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62")
        buf.write("c\63e\64g\65i\66k\67m8o9q:s;u<w=y>{?}@\177\2\u0081A\u0083")
        buf.write("B\u0085C\u0087D\u0089E\u008bF\u008dG\u008fH\u0091I\u0093")
        buf.write("J\u0095K\u0097L\u0099M\u009bN\u009dO\u009fP\u00a1Q\u00a3")
        buf.write("R\u00a5S\u00a7T\u00a9U\u00abV\u00adW\u00afX\u00b1Y\u00b3")
        buf.write("Z\u00b5[\u00b7\\\u00b9]\u00bb^\u00bd_\u00bf`\u00c1a\u00c3")
        buf.write("b\u00c5c\u00c7d\u00c9e\u00cbf\u00cdg\u00cfh\u00d1i\u00d3")
        buf.write("j\u00d5k\u00d7l\u00d9m\u00dbn\u00ddo\u00dfp\u00e1q\u00e3")
        buf.write("r\u00e5s\u00e7t\u00e9u\u00ebv\u00edw\u00ef\2\u00f1x\u00f3")
        buf.write("y\u00f5z\u00f7{\u00f9|\u00fb}\u00fd~\u00ff\177\u0101\2")
        buf.write("\u0103\2\u0105\2\u0107\2\u0109\2\3\2\r\4\2\f\f\16\17\3")
        buf.write("\2\62;\5\2\62;CHch\3\2\62\63\3\2\629\5\2C\\aac|\6\2\62")
        buf.write(";C\\aac|\3\2\60\60\6\2\f\f\16\17))^^\6\2\f\f\16\17$$^")
        buf.write("^\3\2^^\2\u03eb\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2")
        buf.write("\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21")
        buf.write("\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3")
        buf.write("\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2")
        buf.write("\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2")
        buf.write("\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2")
        buf.write("\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2")
        buf.write("\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3")
        buf.write("\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q")
        buf.write("\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2")
        buf.write("[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2")
        buf.write("\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2")
        buf.write("\2\2o\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2")
        buf.write("\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\u0081\3\2\2\2")
        buf.write("\2\u0083\3\2\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089")
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
        buf.write("\2\2\u00d7\3\2\2\2\2\u00d9\3\2\2\2\2\u00db\3\2\2\2\2\u00dd")
        buf.write("\3\2\2\2\2\u00df\3\2\2\2\2\u00e1\3\2\2\2\2\u00e3\3\2\2")
        buf.write("\2\2\u00e5\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9\3\2\2\2\2\u00eb")
        buf.write("\3\2\2\2\2\u00ed\3\2\2\2\2\u00f1\3\2\2\2\2\u00f3\3\2\2")
        buf.write("\2\2\u00f5\3\2\2\2\2\u00f7\3\2\2\2\2\u00f9\3\2\2\2\2\u00fb")
        buf.write("\3\2\2\2\2\u00fd\3\2\2\2\2\u00ff\3\2\2\2\3\u010b\3\2\2")
        buf.write("\2\5\u010f\3\2\2\2\7\u0112\3\2\2\2\t\u0114\3\2\2\2\13")
        buf.write("\u0116\3\2\2\2\r\u0118\3\2\2\2\17\u011a\3\2\2\2\21\u011c")
        buf.write("\3\2\2\2\23\u011f\3\2\2\2\25\u0121\3\2\2\2\27\u0123\3")
        buf.write("\2\2\2\31\u0127\3\2\2\2\33\u012a\3\2\2\2\35\u012d\3\2")
        buf.write("\2\2\37\u0130\3\2\2\2!\u0133\3\2\2\2#\u0136\3\2\2\2%\u0138")
        buf.write("\3\2\2\2\'\u013b\3\2\2\2)\u013d\3\2\2\2+\u0140\3\2\2\2")
        buf.write("-\u0142\3\2\2\2/\u0144\3\2\2\2\61\u0146\3\2\2\2\63\u014a")
        buf.write("\3\2\2\2\65\u014e\3\2\2\2\67\u0152\3\2\2\29\u015a\3\2")
        buf.write("\2\2;\u015e\3\2\2\2=\u0165\3\2\2\2?\u016e\3\2\2\2A\u0179")
        buf.write("\3\2\2\2C\u0185\3\2\2\2E\u018f\3\2\2\2G\u0194\3\2\2\2")
        buf.write("I\u0198\3\2\2\2K\u019d\3\2\2\2M\u01a1\3\2\2\2O\u01a5\3")
        buf.write("\2\2\2Q\u01a9\3\2\2\2S\u01ad\3\2\2\2U\u01b1\3\2\2\2W\u01b5")
        buf.write("\3\2\2\2Y\u01ba\3\2\2\2[\u01be\3\2\2\2]\u01c3\3\2\2\2")
        buf.write("_\u01c7\3\2\2\2a\u01cb\3\2\2\2c\u01ce\3\2\2\2e\u01d1\3")
        buf.write("\2\2\2g\u01d4\3\2\2\2i\u01d7\3\2\2\2k\u01da\3\2\2\2m\u01dd")
        buf.write("\3\2\2\2o\u01e0\3\2\2\2q\u01e4\3\2\2\2s\u01e7\3\2\2\2")
        buf.write("u\u01ec\3\2\2\2w\u01f0\3\2\2\2y\u01f4\3\2\2\2{\u01f9\3")
        buf.write("\2\2\2}\u0219\3\2\2\2\177\u022d\3\2\2\2\u0081\u022f\3")
        buf.write("\2\2\2\u0083\u0231\3\2\2\2\u0085\u0234\3\2\2\2\u0087\u0237")
        buf.write("\3\2\2\2\u0089\u0239\3\2\2\2\u008b\u023c\3\2\2\2\u008d")
        buf.write("\u023e\3\2\2\2\u008f\u0245\3\2\2\2\u0091\u024b\3\2\2\2")
        buf.write("\u0093\u0250\3\2\2\2\u0095\u0253\3\2\2\2\u0097\u025f\3")
        buf.write("\2\2\2\u0099\u0264\3\2\2\2\u009b\u0269\3\2\2\2\u009d\u0270")
        buf.write("\3\2\2\2\u009f\u0274\3\2\2\2\u00a1\u0276\3\2\2\2\u00a3")
        buf.write("\u027c\3\2\2\2\u00a5\u0282\3\2\2\2\u00a7\u0289\3\2\2\2")
        buf.write("\u00a9\u028d\3\2\2\2\u00ab\u0292\3\2\2\2\u00ad\u0297\3")
        buf.write("\2\2\2\u00af\u029b\3\2\2\2\u00b1\u02a1\3\2\2\2\u00b3\u02a9")
        buf.write("\3\2\2\2\u00b5\u02b3\3\2\2\2\u00b7\u02b6\3\2\2\2\u00b9")
        buf.write("\u02be\3\2\2\2\u00bb\u02c9\3\2\2\2\u00bd\u02ce\3\2\2\2")
        buf.write("\u00bf\u02d2\3\2\2\2\u00c1\u02d5\3\2\2\2\u00c3\u02da\3")
        buf.write("\2\2\2\u00c5\u02df\3\2\2\2\u00c7\u02e1\3\2\2\2\u00c9\u02e7")
        buf.write("\3\2\2\2\u00cb\u02ee\3\2\2\2\u00cd\u02f2\3\2\2\2\u00cf")
        buf.write("\u02fa\3\2\2\2\u00d1\u0301\3\2\2\2\u00d3\u0307\3\2\2\2")
        buf.write("\u00d5\u0309\3\2\2\2\u00d7\u030f\3\2\2\2\u00d9\u0312\3")
        buf.write("\2\2\2\u00db\u0317\3\2\2\2\u00dd\u0319\3\2\2\2\u00df\u031e")
        buf.write("\3\2\2\2\u00e1\u0332\3\2\2\2\u00e3\u0334\3\2\2\2\u00e5")
        buf.write("\u0359\3\2\2\2\u00e7\u035b\3\2\2\2\u00e9\u0362\3\2\2\2")
        buf.write("\u00eb\u0367\3\2\2\2\u00ed\u0372\3\2\2\2\u00ef\u037a\3")
        buf.write("\2\2\2\u00f1\u037c\3\2\2\2\u00f3\u037f\3\2\2\2\u00f5\u0382")
        buf.write("\3\2\2\2\u00f7\u0385\3\2\2\2\u00f9\u0388\3\2\2\2\u00fb")
        buf.write("\u038b\3\2\2\2\u00fd\u038e\3\2\2\2\u00ff\u0392\3\2\2\2")
        buf.write("\u0101\u03a6\3\2\2\2\u0103\u03c2\3\2\2\2\u0105\u03c6\3")
        buf.write("\2\2\2\u0107\u03c8\3\2\2\2\u0109\u03ce\3\2\2\2\u010b\u010c")
        buf.write("\7c\2\2\u010c\u010d\7p\2\2\u010d\u010e\7f\2\2\u010e\4")
        buf.write("\3\2\2\2\u010f\u0110\7q\2\2\u0110\u0111\7t\2\2\u0111\6")
        buf.write("\3\2\2\2\u0112\u0113\7(\2\2\u0113\b\3\2\2\2\u0114\u0115")
        buf.write("\7~\2\2\u0115\n\3\2\2\2\u0116\u0117\7`\2\2\u0117\f\3\2")
        buf.write("\2\2\u0118\u0119\7/\2\2\u0119\16\3\2\2\2\u011a\u011b\7")
        buf.write("-\2\2\u011b\20\3\2\2\2\u011c\u011d\7\61\2\2\u011d\u011e")
        buf.write("\7\61\2\2\u011e\22\3\2\2\2\u011f\u0120\7\61\2\2\u0120")
        buf.write("\24\3\2\2\2\u0121\u0122\7\'\2\2\u0122\26\3\2\2\2\u0123")
        buf.write("\u0124\7o\2\2\u0124\u0125\7q\2\2\u0125\u0126\7f\2\2\u0126")
        buf.write("\30\3\2\2\2\u0127\u0128\7,\2\2\u0128\u0129\7,\2\2\u0129")
        buf.write("\32\3\2\2\2\u012a\u012b\7>\2\2\u012b\u012c\7>\2\2\u012c")
        buf.write("\34\3\2\2\2\u012d\u012e\7@\2\2\u012e\u012f\7@\2\2\u012f")
        buf.write("\36\3\2\2\2\u0130\u0131\7?\2\2\u0131\u0132\7?\2\2\u0132")
        buf.write(" \3\2\2\2\u0133\u0134\7#\2\2\u0134\u0135\7?\2\2\u0135")
        buf.write("\"\3\2\2\2\u0136\u0137\7>\2\2\u0137$\3\2\2\2\u0138\u0139")
        buf.write("\7>\2\2\u0139\u013a\7?\2\2\u013a&\3\2\2\2\u013b\u013c")
        buf.write("\7@\2\2\u013c(\3\2\2\2\u013d\u013e\7@\2\2\u013e\u013f")
        buf.write("\7?\2\2\u013f*\3\2\2\2\u0140\u0141\7\u0080\2\2\u0141,")
        buf.write("\3\2\2\2\u0142\u0143\7A\2\2\u0143.\3\2\2\2\u0144\u0145")
        buf.write("\7#\2\2\u0145\60\3\2\2\2\u0146\u0147\7c\2\2\u0147\u0148")
        buf.write("\7d\2\2\u0148\u0149\7u\2\2\u0149\62\3\2\2\2\u014a\u014b")
        buf.write("\7c\2\2\u014b\u014c\7n\2\2\u014c\u014d\7n\2\2\u014d\64")
        buf.write("\3\2\2\2\u014e\u014f\7c\2\2\u014f\u0150\7p\2\2\u0150\u0151")
        buf.write("\7{\2\2\u0151\66\3\2\2\2\u0152\u0153\7c\2\2\u0153\u0154")
        buf.write("\7v\2\2\u0154\u0155\7N\2\2\u0155\u0156\7c\2\2\u0156\u0157")
        buf.write("\7d\2\2\u0157\u0158\7g\2\2\u0158\u0159\7n\2\2\u01598\3")
        buf.write("\2\2\2\u015a\u015b\7d\2\2\u015b\u015c\7k\2\2\u015c\u015d")
        buf.write("\7p\2\2\u015d:\3\2\2\2\u015e\u015f\7e\2\2\u015f\u0160")
        buf.write("\7j\2\2\u0160\u0161\7q\2\2\u0161\u0162\7q\2\2\u0162\u0163")
        buf.write("\7u\2\2\u0163\u0164\7g\2\2\u0164<\3\2\2\2\u0165\u0166")
        buf.write("\7e\2\2\u0166\u0167\7q\2\2\u0167\u0168\7p\2\2\u0168\u0169")
        buf.write("\7v\2\2\u0169\u016a\7g\2\2\u016a\u016b\7z\2\2\u016b\u016c")
        buf.write("\7v\2\2\u016c\u016d\7u\2\2\u016d>\3\2\2\2\u016e\u016f")
        buf.write("\7e\2\2\u016f\u0170\7q\2\2\u0170\u0171\7w\2\2\u0171\u0172")
        buf.write("\7p\2\2\u0172\u0173\7v\2\2\u0173\u0174\7N\2\2\u0174\u0175")
        buf.write("\7c\2\2\u0175\u0176\7d\2\2\u0176\u0177\7g\2\2\u0177\u0178")
        buf.write("\7n\2\2\u0178@\3\2\2\2\u0179\u017a\7i\2\2\u017a\u017b")
        buf.write("\7g\2\2\u017b\u017c\7v\2\2\u017c\u017d\7a\2\2\u017d\u017e")
        buf.write("\7e\2\2\u017e\u017f\7q\2\2\u017f\u0180\7p\2\2\u0180\u0181")
        buf.write("\7v\2\2\u0181\u0182\7g\2\2\u0182\u0183\7z\2\2\u0183\u0184")
        buf.write("\7v\2\2\u0184B\3\2\2\2\u0185\u0186\7i\2\2\u0186\u0187")
        buf.write("\7g\2\2\u0187\u0188\7v\2\2\u0188\u0189\7a\2\2\u0189\u018a")
        buf.write("\7k\2\2\u018a\u018b\7f\2\2\u018b\u018c\7g\2\2\u018c\u018d")
        buf.write("\7p\2\2\u018d\u018e\7v\2\2\u018eD\3\2\2\2\u018f\u0190")
        buf.write("\7j\2\2\u0190\u0191\7c\2\2\u0191\u0192\7u\2\2\u0192\u0193")
        buf.write("\7j\2\2\u0193F\3\2\2\2\u0194\u0195\7j\2\2\u0195\u0196")
        buf.write("\7g\2\2\u0196\u0197\7z\2\2\u0197H\3\2\2\2\u0198\u0199")
        buf.write("\7m\2\2\u0199\u019a\7g\2\2\u019a\u019b\7{\2\2\u019b\u019c")
        buf.write("\7u\2\2\u019cJ\3\2\2\2\u019d\u019e\7n\2\2\u019e\u019f")
        buf.write("\7g\2\2\u019f\u01a0\7p\2\2\u01a0L\3\2\2\2\u01a1\u01a2")
        buf.write("\7o\2\2\u01a2\u01a3\7c\2\2\u01a3\u01a4\7z\2\2\u01a4N\3")
        buf.write("\2\2\2\u01a5\u01a6\7o\2\2\u01a6\u01a7\7k\2\2\u01a7\u01a8")
        buf.write("\7p\2\2\u01a8P\3\2\2\2\u01a9\u01aa\7u\2\2\u01aa\u01ab")
        buf.write("\7g\2\2\u01ab\u01ac\7v\2\2\u01acR\3\2\2\2\u01ad\u01ae")
        buf.write("\7u\2\2\u01ae\u01af\7v\2\2\u01af\u01b0\7t\2\2\u01b0T\3")
        buf.write("\2\2\2\u01b1\u01b2\7u\2\2\u01b2\u01b3\7w\2\2\u01b3\u01b4")
        buf.write("\7o\2\2\u01b4V\3\2\2\2\u01b5\u01b6\7v\2\2\u01b6\u01b7")
        buf.write("\7{\2\2\u01b7\u01b8\7r\2\2\u01b8\u01b9\7g\2\2\u01b9X\3")
        buf.write("\2\2\2\u01ba\u01bb\7g\2\2\u01bb\u01bc\7p\2\2\u01bc\u01bd")
        buf.write("\7f\2\2\u01bdZ\3\2\2\2\u01be\u01bf\7c\2\2\u01bf\u01c0")
        buf.write("\7p\2\2\u01c0\u01c1\7f\2\2\u01c1\u01c2\7?\2\2\u01c2\\")
        buf.write("\3\2\2\2\u01c3\u01c4\7q\2\2\u01c4\u01c5\7t\2\2\u01c5\u01c6")
        buf.write("\7?\2\2\u01c6^\3\2\2\2\u01c7\u01c8\7?\2\2\u01c8\u01c9")
        buf.write("\7@\2\2\u01c9\u01ca\7?\2\2\u01ca`\3\2\2\2\u01cb\u01cc")
        buf.write("\7(\2\2\u01cc\u01cd\7?\2\2\u01cdb\3\2\2\2\u01ce\u01cf")
        buf.write("\7~\2\2\u01cf\u01d0\7?\2\2\u01d0d\3\2\2\2\u01d1\u01d2")
        buf.write("\7`\2\2\u01d2\u01d3\7?\2\2\u01d3f\3\2\2\2\u01d4\u01d5")
        buf.write("\7/\2\2\u01d5\u01d6\7?\2\2\u01d6h\3\2\2\2\u01d7\u01d8")
        buf.write("\7-\2\2\u01d8\u01d9\7?\2\2\u01d9j\3\2\2\2\u01da\u01db")
        buf.write("\7,\2\2\u01db\u01dc\7?\2\2\u01dcl\3\2\2\2\u01dd\u01de")
        buf.write("\7\61\2\2\u01de\u01df\7?\2\2\u01dfn\3\2\2\2\u01e0\u01e1")
        buf.write("\7\61\2\2\u01e1\u01e2\7\61\2\2\u01e2\u01e3\7?\2\2\u01e3")
        buf.write("p\3\2\2\2\u01e4\u01e5\7\'\2\2\u01e5\u01e6\7?\2\2\u01e6")
        buf.write("r\3\2\2\2\u01e7\u01e8\7o\2\2\u01e8\u01e9\7q\2\2\u01e9")
        buf.write("\u01ea\7f\2\2\u01ea\u01eb\7?\2\2\u01ebt\3\2\2\2\u01ec")
        buf.write("\u01ed\7,\2\2\u01ed\u01ee\7,\2\2\u01ee\u01ef\7?\2\2\u01ef")
        buf.write("v\3\2\2\2\u01f0\u01f1\7@\2\2\u01f1\u01f2\7@\2\2\u01f2")
        buf.write("\u01f3\7?\2\2\u01f3x\3\2\2\2\u01f4\u01f5\7>\2\2\u01f5")
        buf.write("\u01f6\7>\2\2\u01f6\u01f7\7?\2\2\u01f7z\3\2\2\2\u01f8")
        buf.write("\u01fa\7\17\2\2\u01f9\u01f8\3\2\2\2\u01f9\u01fa\3\2\2")
        buf.write("\2\u01fa\u01fb\3\2\2\2\u01fb\u0208\7\f\2\2\u01fc\u01fe")
        buf.write("\7\"\2\2\u01fd\u01fc\3\2\2\2\u01fe\u0201\3\2\2\2\u01ff")
        buf.write("\u01fd\3\2\2\2\u01ff\u0200\3\2\2\2\u0200\u0209\3\2\2\2")
        buf.write("\u0201\u01ff\3\2\2\2\u0202\u0204\7\13\2\2\u0203\u0202")
        buf.write("\3\2\2\2\u0204\u0207\3\2\2\2\u0205\u0203\3\2\2\2\u0205")
        buf.write("\u0206\3\2\2\2\u0206\u0209\3\2\2\2\u0207\u0205\3\2\2\2")
        buf.write("\u0208\u01ff\3\2\2\2\u0208\u0205\3\2\2\2\u0209\u020a\3")
        buf.write("\2\2\2\u020a\u020b\b>\2\2\u020b|\3\2\2\2\u020c\u020e\7")
        buf.write("\"\2\2\u020d\u020c\3\2\2\2\u020e\u020f\3\2\2\2\u020f\u020d")
        buf.write("\3\2\2\2\u020f\u0210\3\2\2\2\u0210\u021a\3\2\2\2\u0211")
        buf.write("\u0213\7\13\2\2\u0212\u0211\3\2\2\2\u0213\u0214\3\2\2")
        buf.write("\2\u0214\u0212\3\2\2\2\u0214\u0215\3\2\2\2\u0215\u021a")
        buf.write("\3\2\2\2\u0216\u0217\7^\2\2\u0217\u021a\5{>\2\u0218\u021a")
        buf.write("\5\177@\2\u0219\u020d\3\2\2\2\u0219\u0212\3\2\2\2\u0219")
        buf.write("\u0216\3\2\2\2\u0219\u0218\3\2\2\2\u021a\u021b\3\2\2\2")
        buf.write("\u021b\u021c\b?\3\2\u021c~\3\2\2\2\u021d\u0221\5\u0083")
        buf.write("B\2\u021e\u0220\13\2\2\2\u021f\u021e\3\2\2\2\u0220\u0223")
        buf.write("\3\2\2\2\u0221\u0222\3\2\2\2\u0221\u021f\3\2\2\2\u0222")
        buf.write("\u0224\3\2\2\2\u0223\u0221\3\2\2\2\u0224\u0225\5\u0085")
        buf.write("C\2\u0225\u022e\3\2\2\2\u0226\u022a\5\u0081A\2\u0227\u0229")
        buf.write("\n\2\2\2\u0228\u0227\3\2\2\2\u0229\u022c\3\2\2\2\u022a")
        buf.write("\u0228\3\2\2\2\u022a\u022b\3\2\2\2\u022b\u022e\3\2\2\2")
        buf.write("\u022c\u022a\3\2\2\2\u022d\u021d\3\2\2\2\u022d\u0226\3")
        buf.write("\2\2\2\u022e\u0080\3\2\2\2\u022f\u0230\7%\2\2\u0230\u0082")
        buf.write("\3\2\2\2\u0231\u0232\7*\2\2\u0232\u0233\7,\2\2\u0233\u0084")
        buf.write("\3\2\2\2\u0234\u0235\7,\2\2\u0235\u0236\7+\2\2\u0236\u0086")
        buf.write("\3\2\2\2\u0237\u0238\7,\2\2\u0238\u0088\3\2\2\2\u0239")
        buf.write("\u023a\7c\2\2\u023a\u023b\7u\2\2\u023b\u008a\3\2\2\2\u023c")
        buf.write("\u023d\7\60\2\2\u023d\u008c\3\2\2\2\u023e\u023f\7k\2\2")
        buf.write("\u023f\u0240\7o\2\2\u0240\u0241\7r\2\2\u0241\u0242\7q")
        buf.write("\2\2\u0242\u0243\7t\2\2\u0243\u0244\7v\2\2\u0244\u008e")
        buf.write("\3\2\2\2\u0245\u0246\7r\2\2\u0246\u0247\7t\2\2\u0247\u0248")
        buf.write("\7k\2\2\u0248\u0249\7p\2\2\u0249\u024a\7v\2\2\u024a\u0090")
        buf.write("\3\2\2\2\u024b\u024c\7h\2\2\u024c\u024d\7t\2\2\u024d\u024e")
        buf.write("\7q\2\2\u024e\u024f\7o\2\2\u024f\u0092\3\2\2\2\u0250\u0251")
        buf.write("\7\60\2\2\u0251\u0252\7\60\2\2\u0252\u0094\3\2\2\2\u0253")
        buf.write("\u0254\7u\2\2\u0254\u0255\7g\2\2\u0255\u0256\7v\2\2\u0256")
        buf.write("\u0257\7k\2\2\u0257\u0258\7p\2\2\u0258\u0259\7v\2\2\u0259")
        buf.write("\u025a\7n\2\2\u025a\u025b\7g\2\2\u025b\u025c\7x\2\2\u025c")
        buf.write("\u025d\7g\2\2\u025d\u025e\7n\2\2\u025e\u0096\3\2\2\2\u025f")
        buf.write("\u0260\7u\2\2\u0260\u0261\7c\2\2\u0261\u0262\7x\2\2\u0262")
        buf.write("\u0263\7g\2\2\u0263\u0098\3\2\2\2\u0264\u0265\7u\2\2\u0265")
        buf.write("\u0266\7v\2\2\u0266\u0267\7q\2\2\u0267\u0268\7r\2\2\u0268")
        buf.write("\u009a\3\2\2\2\u0269\u026a\7n\2\2\u026a\u026b\7c\2\2\u026b")
        buf.write("\u026c\7o\2\2\u026c\u026d\7d\2\2\u026d\u026e\7f\2\2\u026e")
        buf.write("\u026f\7c\2\2\u026f\u009c\3\2\2\2\u0270\u0271\7p\2\2\u0271")
        buf.write("\u0272\7q\2\2\u0272\u0273\7v\2\2\u0273\u009e\3\2\2\2\u0274")
        buf.write("\u0275\7.\2\2\u0275\u00a0\3\2\2\2\u0276\u0277\7e\2\2\u0277")
        buf.write("\u0278\7q\2\2\u0278\u0279\7p\2\2\u0279\u027a\7u\2\2\u027a")
        buf.write("\u027b\7v\2\2\u027b\u00a2\3\2\2\2\u027c\u027d\7c\2\2\u027d")
        buf.write("\u027e\7y\2\2\u027e\u027f\7c\2\2\u027f\u0280\7k\2\2\u0280")
        buf.write("\u0281\7v\2\2\u0281\u00a4\3\2\2\2\u0282\u0283\7c\2\2\u0283")
        buf.write("\u0284\7u\2\2\u0284\u0285\7u\2\2\u0285\u0286\7g\2\2\u0286")
        buf.write("\u0287\7t\2\2\u0287\u0288\7v\2\2\u0288\u00a6\3\2\2\2\u0289")
        buf.write("\u028a\7x\2\2\u028a\u028b\7c\2\2\u028b\u028c\7t\2\2\u028c")
        buf.write("\u00a8\3\2\2\2\u028d\u028e\7v\2\2\u028e\u028f\7t\2\2\u028f")
        buf.write("\u0290\7c\2\2\u0290\u0291\7r\2\2\u0291\u00aa\3\2\2\2\u0292")
        buf.write("\u0293\7r\2\2\u0293\u0294\7c\2\2\u0294\u0295\7u\2\2\u0295")
        buf.write("\u0296\7u\2\2\u0296\u00ac\3\2\2\2\u0297\u0298\7f\2\2\u0298")
        buf.write("\u0299\7g\2\2\u0299\u029a\7n\2\2\u029a\u00ae\3\2\2\2\u029b")
        buf.write("\u029c\7u\2\2\u029c\u029d\7r\2\2\u029d\u029e\7c\2\2\u029e")
        buf.write("\u029f\7y\2\2\u029f\u02a0\7p\2\2\u02a0\u00b0\3\2\2\2\u02a1")
        buf.write("\u02a2\7h\2\2\u02a2\u02a3\7k\2\2\u02a3\u02a4\7p\2\2\u02a4")
        buf.write("\u02a5\7c\2\2\u02a5\u02a6\7n\2\2\u02a6\u02a7\7n\2\2\u02a7")
        buf.write("\u02a8\7{\2\2\u02a8\u00b2\3\2\2\2\u02a9\u02aa\7k\2\2\u02aa")
        buf.write("\u02ab\7p\2\2\u02ab\u02ac\7x\2\2\u02ac\u02ad\7c\2\2\u02ad")
        buf.write("\u02ae\7t\2\2\u02ae\u02af\7k\2\2\u02af\u02b0\7c\2\2\u02b0")
        buf.write("\u02b1\7p\2\2\u02b1\u02b2\7v\2\2\u02b2\u00b4\3\2\2\2\u02b3")
        buf.write("\u02b4\7i\2\2\u02b4\u02b5\7q\2\2\u02b5\u00b6\3\2\2\2\u02b6")
        buf.write("\u02b7\7d\2\2\u02b7\u02b8\7w\2\2\u02b8\u02b9\7k\2\2\u02b9")
        buf.write("\u02ba\7n\2\2\u02ba\u02bb\7v\2\2\u02bb\u02bc\7k\2\2\u02bc")
        buf.write("\u02bd\7p\2\2\u02bd\u00b8\3\2\2\2\u02be\u02bf\7u\2\2\u02bf")
        buf.write("\u02c0\7g\2\2\u02c0\u02c1\7s\2\2\u02c1\u02c2\7w\2\2\u02c2")
        buf.write("\u02c3\7g\2\2\u02c3\u02c4\7p\2\2\u02c4\u02c5\7v\2\2\u02c5")
        buf.write("\u02c6\7k\2\2\u02c6\u02c7\7c\2\2\u02c7\u02c8\7n\2\2\u02c8")
        buf.write("\u00ba\3\2\2\2\u02c9\u02ca\7y\2\2\u02ca\u02cb\7j\2\2\u02cb")
        buf.write("\u02cc\7g\2\2\u02cc\u02cd\7p\2\2\u02cd\u00bc\3\2\2\2\u02ce")
        buf.write("\u02cf\7n\2\2\u02cf\u02d0\7g\2\2\u02d0\u02d1\7v\2\2\u02d1")
        buf.write("\u00be\3\2\2\2\u02d2\u02d3\7k\2\2\u02d3\u02d4\7h\2\2\u02d4")
        buf.write("\u00c0\3\2\2\2\u02d5\u02d6\7g\2\2\u02d6\u02d7\7n\2\2\u02d7")
        buf.write("\u02d8\7k\2\2\u02d8\u02d9\7h\2\2\u02d9\u00c2\3\2\2\2\u02da")
        buf.write("\u02db\7g\2\2\u02db\u02dc\7n\2\2\u02dc\u02dd\7u\2\2\u02dd")
        buf.write("\u02de\7g\2\2\u02de\u00c4\3\2\2\2\u02df\u02e0\7B\2\2\u02e0")
        buf.write("\u00c6\3\2\2\2\u02e1\u02e2\7y\2\2\u02e2\u02e3\7j\2\2\u02e3")
        buf.write("\u02e4\7k\2\2\u02e4\u02e5\7n\2\2\u02e5\u02e6\7g\2\2\u02e6")
        buf.write("\u00c8\3\2\2\2\u02e7\u02e8\7i\2\2\u02e8\u02e9\7n\2\2\u02e9")
        buf.write("\u02ea\7q\2\2\u02ea\u02eb\7d\2\2\u02eb\u02ec\7c\2\2\u02ec")
        buf.write("\u02ed\7n\2\2\u02ed\u00ca\3\2\2\2\u02ee\u02ef\7f\2\2\u02ef")
        buf.write("\u02f0\7g\2\2\u02f0\u02f1\7h\2\2\u02f1\u00cc\3\2\2\2\u02f2")
        buf.write("\u02f3\7t\2\2\u02f3\u02f4\7g\2\2\u02f4\u02f5\7v\2\2\u02f5")
        buf.write("\u02f6\7w\2\2\u02f6\u02f7\7t\2\2\u02f7\u02f8\7p\2\2\u02f8")
        buf.write("\u02f9\7u\2\2\u02f9\u00ce\3\2\2\2\u02fa\u02fb\7g\2\2\u02fb")
        buf.write("\u02fc\7z\2\2\u02fc\u02fd\7k\2\2\u02fd\u02fe\7u\2\2\u02fe")
        buf.write("\u02ff\7v\2\2\u02ff\u0300\7u\2\2\u0300\u00d0\3\2\2\2\u0301")
        buf.write("\u0302\7y\2\2\u0302\u0303\7j\2\2\u0303\u0304\7g\2\2\u0304")
        buf.write("\u0305\7t\2\2\u0305\u0306\7g\2\2\u0306\u00d2\3\2\2\2\u0307")
        buf.write("\u0308\7?\2\2\u0308\u00d4\3\2\2\2\u0309\u030a\7h\2\2\u030a")
        buf.write("\u030b\7q\2\2\u030b\u030c\7t\2\2\u030c\u030d\3\2\2\2\u030d")
        buf.write("\u030e\bk\4\2\u030e\u00d6\3\2\2\2\u030f\u0310\7?\2\2\u0310")
        buf.write("\u0311\7@\2\2\u0311\u00d8\3\2\2\2\u0312\u0313\7k\2\2\u0313")
        buf.write("\u0314\7p\2\2\u0314\u0315\3\2\2\2\u0315\u0316\bm\5\2\u0316")
        buf.write("\u00da\3\2\2\2\u0317\u0318\7<\2\2\u0318\u00dc\3\2\2\2")
        buf.write("\u0319\u031a\7P\2\2\u031a\u031b\7q\2\2\u031b\u031c\7p")
        buf.write("\2\2\u031c\u031d\7g\2\2\u031d\u00de\3\2\2\2\u031e\u031f")
        buf.write("\7c\2\2\u031f\u0320\7v\2\2\u0320\u0321\7q\2\2\u0321\u0322")
        buf.write("\7o\2\2\u0322\u0323\7k\2\2\u0323\u0324\7e\2\2\u0324\u0325")
        buf.write("\7c\2\2\u0325\u0326\7n\2\2\u0326\u0327\7n\2\2\u0327\u0328")
        buf.write("\7{\2\2\u0328\u00e0\3\2\2\2\u0329\u032a\7H\2\2\u032a\u032b")
        buf.write("\7c\2\2\u032b\u032c\7n\2\2\u032c\u032d\7u\2\2\u032d\u0333")
        buf.write("\7g\2\2\u032e\u032f\7V\2\2\u032f\u0330\7t\2\2\u0330\u0331")
        buf.write("\7w\2\2\u0331\u0333\7g\2\2\u0332\u0329\3\2\2\2\u0332\u032e")
        buf.write("\3\2\2\2\u0333\u00e2\3\2\2\2\u0334\u0335\7g\2\2\u0335")
        buf.write("\u0336\7v\2\2\u0336\u0337\7g\2\2\u0337\u0338\7t\2\2\u0338")
        buf.write("\u0339\7p\2\2\u0339\u033a\7c\2\2\u033a\u033b\7n\2\2\u033b")
        buf.write("\u00e4\3\2\2\2\u033c\u033e\t\3\2\2\u033d\u033c\3\2\2\2")
        buf.write("\u033e\u033f\3\2\2\2\u033f\u033d\3\2\2\2\u033f\u0340\3")
        buf.write("\2\2\2\u0340\u035a\3\2\2\2\u0341\u0342\7\62\2\2\u0342")
        buf.write("\u0343\7z\2\2\u0343\u0345\3\2\2\2\u0344\u0346\t\4\2\2")
        buf.write("\u0345\u0344\3\2\2\2\u0346\u0347\3\2\2\2\u0347\u0345\3")
        buf.write("\2\2\2\u0347\u0348\3\2\2\2\u0348\u035a\3\2\2\2\u0349\u034a")
        buf.write("\7\62\2\2\u034a\u034b\7d\2\2\u034b\u034d\3\2\2\2\u034c")
        buf.write("\u034e\t\5\2\2\u034d\u034c\3\2\2\2\u034e\u034f\3\2\2\2")
        buf.write("\u034f\u034d\3\2\2\2\u034f\u0350\3\2\2\2\u0350\u035a\3")
        buf.write("\2\2\2\u0351\u0352\7\62\2\2\u0352\u0353\7q\2\2\u0353\u0355")
        buf.write("\3\2\2\2\u0354\u0356\t\6\2\2\u0355\u0354\3\2\2\2\u0356")
        buf.write("\u0357\3\2\2\2\u0357\u0355\3\2\2\2\u0357\u0358\3\2\2\2")
        buf.write("\u0358\u035a\3\2\2\2\u0359\u033d\3\2\2\2\u0359\u0341\3")
        buf.write("\2\2\2\u0359\u0349\3\2\2\2\u0359\u0351\3\2\2\2\u035a\u00e6")
        buf.write("\3\2\2\2\u035b\u035f\t\7\2\2\u035c\u035e\t\b\2\2\u035d")
        buf.write("\u035c\3\2\2\2\u035e\u0361\3\2\2\2\u035f\u035d\3\2\2\2")
        buf.write("\u035f\u0360\3\2\2\2\u0360\u00e8\3\2\2\2\u0361\u035f\3")
        buf.write("\2\2\2\u0362\u0365\t\t\2\2\u0363\u0366\5\u00edw\2\u0364")
        buf.write("\u0366\5\u00e7t\2\u0365\u0363\3\2\2\2\u0365\u0364\3\2")
        buf.write("\2\2\u0366\u00ea\3\2\2\2\u0367\u0368\7/\2\2\u0368\u0369")
        buf.write("\7@\2\2\u0369\u036d\3\2\2\2\u036a\u036c\7\"\2\2\u036b")
        buf.write("\u036a\3\2\2\2\u036c\u036f\3\2\2\2\u036d\u036b\3\2\2\2")
        buf.write("\u036d\u036e\3\2\2\2\u036e\u0370\3\2\2\2\u036f\u036d\3")
        buf.write("\2\2\2\u0370\u0371\5\u00e7t\2\u0371\u00ec\3\2\2\2\u0372")
        buf.write("\u0373\7\62\2\2\u0373\u0374\7Z\2\2\u0374\u0376\3\2\2\2")
        buf.write("\u0375\u0377\5\u00efx\2\u0376\u0375\3\2\2\2\u0377\u0378")
        buf.write("\3\2\2\2\u0378\u0376\3\2\2\2\u0378\u0379\3\2\2\2\u0379")
        buf.write("\u00ee\3\2\2\2\u037a\u037b\t\4\2\2\u037b\u00f0\3\2\2\2")
        buf.write("\u037c\u037d\7]\2\2\u037d\u037e\by\6\2\u037e\u00f2\3\2")
        buf.write("\2\2\u037f\u0380\7_\2\2\u0380\u0381\bz\7\2\u0381\u00f4")
        buf.write("\3\2\2\2\u0382\u0383\7}\2\2\u0383\u0384\b{\b\2\u0384\u00f6")
        buf.write("\3\2\2\2\u0385\u0386\7\177\2\2\u0386\u0387\b|\t\2\u0387")
        buf.write("\u00f8\3\2\2\2\u0388\u0389\7*\2\2\u0389\u038a\b}\n\2\u038a")
        buf.write("\u00fa\3\2\2\2\u038b\u038c\7+\2\2\u038c\u038d\b~\13\2")
        buf.write("\u038d\u00fc\3\2\2\2\u038e\u038f\7=\2\2\u038f\u00fe\3")
        buf.write("\2\2\2\u0390\u0393\5\u0101\u0081\2\u0391\u0393\5\u0103")
        buf.write("\u0082\2\u0392\u0390\3\2\2\2\u0392\u0391\3\2\2\2\u0393")
        buf.write("\u0100\3\2\2\2\u0394\u0399\7)\2\2\u0395\u0398\5\u0109")
        buf.write("\u0085\2\u0396\u0398\n\n\2\2\u0397\u0395\3\2\2\2\u0397")
        buf.write("\u0396\3\2\2\2\u0398\u039b\3\2\2\2\u0399\u0397\3\2\2\2")
        buf.write("\u0399\u039a\3\2\2\2\u039a\u039c\3\2\2\2\u039b\u0399\3")
        buf.write("\2\2\2\u039c\u03a7\7)\2\2\u039d\u03a2\7$\2\2\u039e\u03a1")
        buf.write("\5\u0109\u0085\2\u039f\u03a1\n\13\2\2\u03a0\u039e\3\2")
        buf.write("\2\2\u03a0\u039f\3\2\2\2\u03a1\u03a4\3\2\2\2\u03a2\u03a0")
        buf.write("\3\2\2\2\u03a2\u03a3\3\2\2\2\u03a3\u03a5\3\2\2\2\u03a4")
        buf.write("\u03a2\3\2\2\2\u03a5\u03a7\7$\2\2\u03a6\u0394\3\2\2\2")
        buf.write("\u03a6\u039d\3\2\2\2\u03a7\u0102\3\2\2\2\u03a8\u03a9\7")
        buf.write(")\2\2\u03a9\u03aa\7)\2\2\u03aa\u03ab\7)\2\2\u03ab\u03af")
        buf.write("\3\2\2\2\u03ac\u03ae\5\u0105\u0083\2\u03ad\u03ac\3\2\2")
        buf.write("\2\u03ae\u03b1\3\2\2\2\u03af\u03b0\3\2\2\2\u03af\u03ad")
        buf.write("\3\2\2\2\u03b0\u03b2\3\2\2\2\u03b1\u03af\3\2\2\2\u03b2")
        buf.write("\u03b3\7)\2\2\u03b3\u03b4\7)\2\2\u03b4\u03c3\7)\2\2\u03b5")
        buf.write("\u03b6\7$\2\2\u03b6\u03b7\7$\2\2\u03b7\u03b8\7$\2\2\u03b8")
        buf.write("\u03bc\3\2\2\2\u03b9\u03bb\5\u0105\u0083\2\u03ba\u03b9")
        buf.write("\3\2\2\2\u03bb\u03be\3\2\2\2\u03bc\u03bd\3\2\2\2\u03bc")
        buf.write("\u03ba\3\2\2\2\u03bd\u03bf\3\2\2\2\u03be\u03bc\3\2\2\2")
        buf.write("\u03bf\u03c0\7$\2\2\u03c0\u03c1\7$\2\2\u03c1\u03c3\7$")
        buf.write("\2\2\u03c2\u03a8\3\2\2\2\u03c2\u03b5\3\2\2\2\u03c3\u0104")
        buf.write("\3\2\2\2\u03c4\u03c7\5\u0107\u0084\2\u03c5\u03c7\5\u0109")
        buf.write("\u0085\2\u03c6\u03c4\3\2\2\2\u03c6\u03c5\3\2\2\2\u03c7")
        buf.write("\u0106\3\2\2\2\u03c8\u03c9\n\f\2\2\u03c9\u0108\3\2\2\2")
        buf.write("\u03ca\u03cb\7^\2\2\u03cb\u03cf\13\2\2\2\u03cc\u03cd\7")
        buf.write("^\2\2\u03cd\u03cf\5{>\2\u03ce\u03ca\3\2\2\2\u03ce\u03cc")
        buf.write("\3\2\2\2\u03cf\u010a\3\2\2\2\"\2\u01f9\u01ff\u0205\u0208")
        buf.write("\u020f\u0214\u0219\u0221\u022a\u022d\u0332\u033f\u0347")
        buf.write("\u034f\u0357\u0359\u035f\u0365\u036d\u0378\u0392\u0397")
        buf.write("\u0399\u03a0\u03a2\u03a6\u03af\u03bc\u03c2\u03c6\u03ce")
        buf.write("\f\3>\2\b\2\2\3k\3\3m\4\3y\5\3z\6\3{\7\3|\b\3}\t\3~\n")
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
    NL = 61
    WS = 62
    COMMENT_START = 63
    OPEN_MULTI_COMMENT = 64
    CLOSE_MULTI_COMMENT = 65
    STAR = 66
    AS = 67
    DOT = 68
    IMPORT = 69
    PRINT = 70
    FROM = 71
    RANGE = 72
    SETINTLEVEL = 73
    SAVE = 74
    STOP = 75
    LAMBDA = 76
    NOT = 77
    COMMA = 78
    CONST = 79
    AWAIT = 80
    ASSERT = 81
    VAR = 82
    TRAP = 83
    PASS = 84
    DEL = 85
    SPAWN = 86
    FINALLY = 87
    INVARIANT = 88
    GO = 89
    BUILTIN = 90
    SEQUENTIAL = 91
    WHEN = 92
    LET = 93
    IF = 94
    ELIF = 95
    ELSE = 96
    AT = 97
    WHILE = 98
    GLOBAL = 99
    DEF = 100
    RETURNS = 101
    EXISTS = 102
    WHERE = 103
    EQ = 104
    FOR = 105
    IMPLIES = 106
    IN = 107
    COLON = 108
    NONE = 109
    ATOMICALLY = 110
    BOOL = 111
    ETERNAL = 112
    INT = 113
    NAME = 114
    ATOM = 115
    ARROWID = 116
    HEX_INTEGER = 117
    OPEN_BRACK = 118
    CLOSE_BRACK = 119
    OPEN_BRACES = 120
    CLOSE_BRACES = 121
    OPEN_PAREN = 122
    CLOSE_PAREN = 123
    SEMI_COLON = 124
    STRING = 125

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'or'", "'&'", "'|'", "'^'", "'-'", "'+'", "'//'", 
            "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", "'!='", 
            "'<'", "'<='", "'>'", "'>='", "'~'", "'?'", "'!'", "'abs'", 
            "'all'", "'any'", "'atLabel'", "'bin'", "'choose'", "'contexts'", 
            "'countLabel'", "'get_context'", "'get_ident'", "'hash'", "'hex'", 
            "'keys'", "'len'", "'max'", "'min'", "'set'", "'str'", "'sum'", 
            "'type'", "'end'", "'and='", "'or='", "'=>='", "'&='", "'|='", 
            "'^='", "'-='", "'+='", "'*='", "'/='", "'//='", "'%='", "'mod='", 
            "'**='", "'>>='", "'<<='", "'#'", "'(*'", "'*)'", "'*'", "'as'", 
            "'.'", "'import'", "'print'", "'from'", "'..'", "'setintlevel'", 
            "'save'", "'stop'", "'lambda'", "'not'", "','", "'const'", "'await'", 
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
                  "T__56", "T__57", "T__58", "T__59", "NL", "WS", "COMMENT", 
                  "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
                  "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", "RANGE", 
                  "SETINTLEVEL", "SAVE", "STOP", "LAMBDA", "NOT", "COMMA", 
                  "CONST", "AWAIT", "ASSERT", "VAR", "TRAP", "PASS", "DEL", 
                  "SPAWN", "FINALLY", "INVARIANT", "GO", "BUILTIN", "SEQUENTIAL", 
                  "WHEN", "LET", "IF", "ELIF", "ELSE", "AT", "WHILE", "GLOBAL", 
                  "DEF", "RETURNS", "EXISTS", "WHERE", "EQ", "FOR", "IMPLIES", 
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
            actions[60] = self.NL_action 
            actions[105] = self.FOR_action 
            actions[107] = self.IN_action 
            actions[119] = self.OPEN_BRACK_action 
            actions[120] = self.CLOSE_BRACK_action 
            actions[121] = self.OPEN_BRACES_action 
            actions[122] = self.CLOSE_BRACES_action 
            actions[123] = self.OPEN_PAREN_action 
            actions[124] = self.CLOSE_PAREN_action 
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
     


