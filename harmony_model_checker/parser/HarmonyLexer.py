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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\u0082")
        buf.write("\u03e0\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("\t\u0087\4\u0088\t\u0088\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3")
        buf.write("\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\t\3\n")
        buf.write("\3\n\3\13\3\13\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3")
        buf.write("\16\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21\3\22")
        buf.write("\3\22\3\23\3\23\3\23\3\24\3\24\3\25\3\25\3\25\3\26\3\26")
        buf.write("\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3\32\3\32\3\32\3\32")
        buf.write("\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\35\3\35\3\35")
        buf.write("\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\37\3\37\3\37")
        buf.write("\3\37\3\37\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3 \3 \3 \3")
        buf.write(" \3 \3 \3 \3 \3!\3!\3!\3!\3!\3!\3!\3!\3!\3!\3\"\3\"\3")
        buf.write("\"\3\"\3\"\3#\3#\3#\3#\3$\3$\3$\3$\3%\3%\3%\3%\3%\3&\3")
        buf.write("&\3&\3&\3\'\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3)\3)\3)\3)\3")
        buf.write("*\3*\3*\3*\3+\3+\3+\3+\3+\3+\3+\3+\3+\3,\3,\3,\3,\3-\3")
        buf.write("-\3-\3-\3-\3-\3-\3.\3.\3.\3.\3/\3/\3/\3/\3\60\3\60\3\60")
        buf.write("\3\60\3\60\3\61\3\61\3\61\3\61\3\62\3\62\3\62\3\62\3\62")
        buf.write("\3\63\3\63\3\63\3\63\3\64\3\64\3\64\3\64\3\65\3\65\3\65")
        buf.write("\3\66\3\66\3\66\3\67\3\67\3\67\38\38\38\39\39\39\3:\3")
        buf.write(":\3:\3;\3;\3;\3<\3<\3<\3<\3=\3=\3=\3>\3>\3>\3>\3>\3?\3")
        buf.write("?\3?\3?\3@\3@\3@\3@\3A\3A\3A\3A\3B\5B\u020d\nB\3B\3B\7")
        buf.write("B\u0211\nB\fB\16B\u0214\13B\3B\7B\u0217\nB\fB\16B\u021a")
        buf.write("\13B\5B\u021c\nB\3B\3B\3C\6C\u0221\nC\rC\16C\u0222\3C")
        buf.write("\6C\u0226\nC\rC\16C\u0227\3C\3C\3C\5C\u022d\nC\3C\3C\3")
        buf.write("D\3D\7D\u0233\nD\fD\16D\u0236\13D\3D\3D\3D\3D\7D\u023c")
        buf.write("\nD\fD\16D\u023f\13D\5D\u0241\nD\3E\3E\3F\3F\3F\3G\3G")
        buf.write("\3G\3H\3H\3I\3I\3I\3J\3J\3K\3K\3K\3K\3K\3K\3K\3L\3L\3")
        buf.write("L\3L\3L\3L\3M\3M\3M\3M\3M\3N\3N\3N\3O\3O\3O\3O\3O\3O\3")
        buf.write("O\3O\3O\3O\3O\3O\3P\3P\3P\3P\3P\3Q\3Q\3Q\3Q\3Q\3R\3R\3")
        buf.write("R\3R\3R\3R\3R\3S\3S\3S\3S\3T\3T\3U\3U\3U\3U\3U\3U\3V\3")
        buf.write("V\3V\3V\3V\3V\3W\3W\3W\3W\3W\3W\3W\3X\3X\3X\3X\3Y\3Y\3")
        buf.write("Y\3Y\3Y\3Z\3Z\3Z\3Z\3Z\3[\3[\3[\3[\3\\\3\\\3\\\3\\\3\\")
        buf.write("\3\\\3]\3]\3]\3]\3]\3]\3]\3]\3^\3^\3^\3^\3^\3^\3^\3^\3")
        buf.write("^\3^\3_\3_\3_\3`\3`\3`\3`\3`\3`\3`\3`\3a\3a\3a\3a\3a\3")
        buf.write("a\3a\3a\3a\3a\3a\3b\3b\3b\3b\3b\3c\3c\3c\3c\3d\3d\3d\3")
        buf.write("e\3e\3e\3e\3e\3f\3f\3f\3f\3f\3g\3g\3h\3h\3h\3h\3h\3h\3")
        buf.write("i\3i\3i\3i\3i\3i\3i\3j\3j\3j\3j\3k\3k\3k\3k\3k\3k\3k\3")
        buf.write("k\3l\3l\3l\3l\3l\3l\3l\3m\3m\3m\3m\3m\3m\3n\3n\3o\3o\3")
        buf.write("o\3o\3o\3o\3p\3p\3p\3p\3p\3q\3q\3r\3r\3r\3r\3r\3s\3s\3")
        buf.write("s\3s\3s\3s\3s\3s\3s\3s\3s\3t\3t\3t\3t\3t\3t\3t\3t\3t\5")
        buf.write("t\u0343\nt\3u\3u\3u\3u\3u\3u\3u\3u\3v\6v\u034e\nv\rv\16")
        buf.write("v\u034f\3v\3v\3v\3v\6v\u0356\nv\rv\16v\u0357\3v\3v\3v")
        buf.write("\3v\6v\u035e\nv\rv\16v\u035f\3v\3v\3v\3v\6v\u0366\nv\r")
        buf.write("v\16v\u0367\5v\u036a\nv\3w\3w\7w\u036e\nw\fw\16w\u0371")
        buf.write("\13w\3x\3x\3x\5x\u0376\nx\3y\3y\3y\3y\7y\u037c\ny\fy\16")
        buf.write("y\u037f\13y\3y\3y\3z\3z\3z\3z\6z\u0387\nz\rz\16z\u0388")
        buf.write("\3{\3{\3|\3|\3|\3}\3}\3}\3~\3~\3~\3\177\3\177\3\177\3")
        buf.write("\u0080\3\u0080\3\u0080\3\u0081\3\u0081\3\u0081\3\u0082")
        buf.write("\3\u0082\3\u0083\3\u0083\5\u0083\u03a3\n\u0083\3\u0084")
        buf.write("\3\u0084\3\u0084\7\u0084\u03a8\n\u0084\f\u0084\16\u0084")
        buf.write("\u03ab\13\u0084\3\u0084\3\u0084\3\u0084\3\u0084\7\u0084")
        buf.write("\u03b1\n\u0084\f\u0084\16\u0084\u03b4\13\u0084\3\u0084")
        buf.write("\5\u0084\u03b7\n\u0084\3\u0085\3\u0085\3\u0085\3\u0085")
        buf.write("\3\u0085\7\u0085\u03be\n\u0085\f\u0085\16\u0085\u03c1")
        buf.write("\13\u0085\3\u0085\3\u0085\3\u0085\3\u0085\3\u0085\3\u0085")
        buf.write("\3\u0085\3\u0085\7\u0085\u03cb\n\u0085\f\u0085\16\u0085")
        buf.write("\u03ce\13\u0085\3\u0085\3\u0085\3\u0085\5\u0085\u03d3")
        buf.write("\n\u0085\3\u0086\3\u0086\5\u0086\u03d7\n\u0086\3\u0087")
        buf.write("\3\u0087\3\u0088\3\u0088\3\u0088\3\u0088\5\u0088\u03df")
        buf.write("\n\u0088\5\u0234\u03bf\u03cc\2\u0089\3\3\5\4\7\5\t\6\13")
        buf.write("\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37")
        buf.write("\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34")
        buf.write("\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_")
        buf.write("\61a\62c\63e\64g\65i\66k\67m8o9q:s;u<w=y>{?}@\177A\u0081")
        buf.write("B\u0083C\u0085D\u0087\2\u0089E\u008bF\u008dG\u008fH\u0091")
        buf.write("I\u0093J\u0095K\u0097L\u0099M\u009bN\u009dO\u009fP\u00a1")
        buf.write("Q\u00a3R\u00a5S\u00a7T\u00a9U\u00abV\u00adW\u00afX\u00b1")
        buf.write("Y\u00b3Z\u00b5[\u00b7\\\u00b9]\u00bb^\u00bd_\u00bf`\u00c1")
        buf.write("a\u00c3b\u00c5c\u00c7d\u00c9e\u00cbf\u00cdg\u00cfh\u00d1")
        buf.write("i\u00d3j\u00d5k\u00d7l\u00d9m\u00dbn\u00ddo\u00dfp\u00e1")
        buf.write("q\u00e3r\u00e5s\u00e7t\u00e9u\u00ebv\u00edw\u00efx\u00f1")
        buf.write("y\u00f3z\u00f5\2\u00f7{\u00f9|\u00fb}\u00fd~\u00ff\177")
        buf.write("\u0101\u0080\u0103\u0081\u0105\u0082\u0107\2\u0109\2\u010b")
        buf.write("\2\u010d\2\u010f\2\3\2\r\4\2\f\f\16\17\3\2\62;\5\2\62")
        buf.write(";CHch\3\2\62\63\3\2\629\5\2C\\aac|\6\2\62;C\\aac|\3\2")
        buf.write("\60\60\6\2\f\f\16\17))^^\6\2\f\f\16\17$$^^\3\2^^\2\u03fb")
        buf.write("\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13")
        buf.write("\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3")
        buf.write("\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2")
        buf.write("\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2")
        buf.write("%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2")
        buf.write("\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67")
        buf.write("\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2")
        buf.write("A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2")
        buf.write("\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2")
        buf.write("\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2")
        buf.write("\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3")
        buf.write("\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q")
        buf.write("\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2")
        buf.write("{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083")
        buf.write("\3\2\2\2\2\u0085\3\2\2\2\2\u0089\3\2\2\2\2\u008b\3\2\2")
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
        buf.write("\3\2\2\2\2\u00db\3\2\2\2\2\u00dd\3\2\2\2\2\u00df\3\2\2")
        buf.write("\2\2\u00e1\3\2\2\2\2\u00e3\3\2\2\2\2\u00e5\3\2\2\2\2\u00e7")
        buf.write("\3\2\2\2\2\u00e9\3\2\2\2\2\u00eb\3\2\2\2\2\u00ed\3\2\2")
        buf.write("\2\2\u00ef\3\2\2\2\2\u00f1\3\2\2\2\2\u00f3\3\2\2\2\2\u00f7")
        buf.write("\3\2\2\2\2\u00f9\3\2\2\2\2\u00fb\3\2\2\2\2\u00fd\3\2\2")
        buf.write("\2\2\u00ff\3\2\2\2\2\u0101\3\2\2\2\2\u0103\3\2\2\2\2\u0105")
        buf.write("\3\2\2\2\3\u0111\3\2\2\2\5\u0115\3\2\2\2\7\u0118\3\2\2")
        buf.write("\2\t\u011a\3\2\2\2\13\u011c\3\2\2\2\r\u011e\3\2\2\2\17")
        buf.write("\u0120\3\2\2\2\21\u0122\3\2\2\2\23\u0125\3\2\2\2\25\u0127")
        buf.write("\3\2\2\2\27\u0129\3\2\2\2\31\u012d\3\2\2\2\33\u0130\3")
        buf.write("\2\2\2\35\u0133\3\2\2\2\37\u0136\3\2\2\2!\u0139\3\2\2")
        buf.write("\2#\u013c\3\2\2\2%\u013e\3\2\2\2\'\u0141\3\2\2\2)\u0143")
        buf.write("\3\2\2\2+\u0146\3\2\2\2-\u0149\3\2\2\2/\u014b\3\2\2\2")
        buf.write("\61\u014d\3\2\2\2\63\u014f\3\2\2\2\65\u0153\3\2\2\2\67")
        buf.write("\u0157\3\2\2\29\u015b\3\2\2\2;\u015f\3\2\2\2=\u0166\3")
        buf.write("\2\2\2?\u016f\3\2\2\2A\u017b\3\2\2\2C\u0185\3\2\2\2E\u018a")
        buf.write("\3\2\2\2G\u018e\3\2\2\2I\u0192\3\2\2\2K\u0197\3\2\2\2")
        buf.write("M\u019b\3\2\2\2O\u01a0\3\2\2\2Q\u01a4\3\2\2\2S\u01a8\3")
        buf.write("\2\2\2U\u01ac\3\2\2\2W\u01b5\3\2\2\2Y\u01b9\3\2\2\2[\u01c0")
        buf.write("\3\2\2\2]\u01c4\3\2\2\2_\u01c8\3\2\2\2a\u01cd\3\2\2\2")
        buf.write("c\u01d1\3\2\2\2e\u01d6\3\2\2\2g\u01da\3\2\2\2i\u01de\3")
        buf.write("\2\2\2k\u01e1\3\2\2\2m\u01e4\3\2\2\2o\u01e7\3\2\2\2q\u01ea")
        buf.write("\3\2\2\2s\u01ed\3\2\2\2u\u01f0\3\2\2\2w\u01f3\3\2\2\2")
        buf.write("y\u01f7\3\2\2\2{\u01fa\3\2\2\2}\u01ff\3\2\2\2\177\u0203")
        buf.write("\3\2\2\2\u0081\u0207\3\2\2\2\u0083\u020c\3\2\2\2\u0085")
        buf.write("\u022c\3\2\2\2\u0087\u0240\3\2\2\2\u0089\u0242\3\2\2\2")
        buf.write("\u008b\u0244\3\2\2\2\u008d\u0247\3\2\2\2\u008f\u024a\3")
        buf.write("\2\2\2\u0091\u024c\3\2\2\2\u0093\u024f\3\2\2\2\u0095\u0251")
        buf.write("\3\2\2\2\u0097\u0258\3\2\2\2\u0099\u025e\3\2\2\2\u009b")
        buf.write("\u0263\3\2\2\2\u009d\u0266\3\2\2\2\u009f\u0272\3\2\2\2")
        buf.write("\u00a1\u0277\3\2\2\2\u00a3\u027c\3\2\2\2\u00a5\u0283\3")
        buf.write("\2\2\2\u00a7\u0287\3\2\2\2\u00a9\u0289\3\2\2\2\u00ab\u028f")
        buf.write("\3\2\2\2\u00ad\u0295\3\2\2\2\u00af\u029c\3\2\2\2\u00b1")
        buf.write("\u02a0\3\2\2\2\u00b3\u02a5\3\2\2\2\u00b5\u02aa\3\2\2\2")
        buf.write("\u00b7\u02ae\3\2\2\2\u00b9\u02b4\3\2\2\2\u00bb\u02bc\3")
        buf.write("\2\2\2\u00bd\u02c6\3\2\2\2\u00bf\u02c9\3\2\2\2\u00c1\u02d1")
        buf.write("\3\2\2\2\u00c3\u02dc\3\2\2\2\u00c5\u02e1\3\2\2\2\u00c7")
        buf.write("\u02e5\3\2\2\2\u00c9\u02e8\3\2\2\2\u00cb\u02ed\3\2\2\2")
        buf.write("\u00cd\u02f2\3\2\2\2\u00cf\u02f4\3\2\2\2\u00d1\u02fa\3")
        buf.write("\2\2\2\u00d3\u0301\3\2\2\2\u00d5\u0305\3\2\2\2\u00d7\u030d")
        buf.write("\3\2\2\2\u00d9\u0314\3\2\2\2\u00db\u031a\3\2\2\2\u00dd")
        buf.write("\u031c\3\2\2\2\u00df\u0322\3\2\2\2\u00e1\u0327\3\2\2\2")
        buf.write("\u00e3\u0329\3\2\2\2\u00e5\u032e\3\2\2\2\u00e7\u0342\3")
        buf.write("\2\2\2\u00e9\u0344\3\2\2\2\u00eb\u0369\3\2\2\2\u00ed\u036b")
        buf.write("\3\2\2\2\u00ef\u0372\3\2\2\2\u00f1\u0377\3\2\2\2\u00f3")
        buf.write("\u0382\3\2\2\2\u00f5\u038a\3\2\2\2\u00f7\u038c\3\2\2\2")
        buf.write("\u00f9\u038f\3\2\2\2\u00fb\u0392\3\2\2\2\u00fd\u0395\3")
        buf.write("\2\2\2\u00ff\u0398\3\2\2\2\u0101\u039b\3\2\2\2\u0103\u039e")
        buf.write("\3\2\2\2\u0105\u03a2\3\2\2\2\u0107\u03b6\3\2\2\2\u0109")
        buf.write("\u03d2\3\2\2\2\u010b\u03d6\3\2\2\2\u010d\u03d8\3\2\2\2")
        buf.write("\u010f\u03de\3\2\2\2\u0111\u0112\7c\2\2\u0112\u0113\7")
        buf.write("p\2\2\u0113\u0114\7f\2\2\u0114\4\3\2\2\2\u0115\u0116\7")
        buf.write("q\2\2\u0116\u0117\7t\2\2\u0117\6\3\2\2\2\u0118\u0119\7")
        buf.write("(\2\2\u0119\b\3\2\2\2\u011a\u011b\7~\2\2\u011b\n\3\2\2")
        buf.write("\2\u011c\u011d\7`\2\2\u011d\f\3\2\2\2\u011e\u011f\7/\2")
        buf.write("\2\u011f\16\3\2\2\2\u0120\u0121\7-\2\2\u0121\20\3\2\2")
        buf.write("\2\u0122\u0123\7\61\2\2\u0123\u0124\7\61\2\2\u0124\22")
        buf.write("\3\2\2\2\u0125\u0126\7\61\2\2\u0126\24\3\2\2\2\u0127\u0128")
        buf.write("\7\'\2\2\u0128\26\3\2\2\2\u0129\u012a\7o\2\2\u012a\u012b")
        buf.write("\7q\2\2\u012b\u012c\7f\2\2\u012c\30\3\2\2\2\u012d\u012e")
        buf.write("\7,\2\2\u012e\u012f\7,\2\2\u012f\32\3\2\2\2\u0130\u0131")
        buf.write("\7>\2\2\u0131\u0132\7>\2\2\u0132\34\3\2\2\2\u0133\u0134")
        buf.write("\7@\2\2\u0134\u0135\7@\2\2\u0135\36\3\2\2\2\u0136\u0137")
        buf.write("\7?\2\2\u0137\u0138\7?\2\2\u0138 \3\2\2\2\u0139\u013a")
        buf.write("\7#\2\2\u013a\u013b\7?\2\2\u013b\"\3\2\2\2\u013c\u013d")
        buf.write("\7>\2\2\u013d$\3\2\2\2\u013e\u013f\7>\2\2\u013f\u0140")
        buf.write("\7?\2\2\u0140&\3\2\2\2\u0141\u0142\7@\2\2\u0142(\3\2\2")
        buf.write("\2\u0143\u0144\7@\2\2\u0144\u0145\7?\2\2\u0145*\3\2\2")
        buf.write("\2\u0146\u0147\7?\2\2\u0147\u0148\7@\2\2\u0148,\3\2\2")
        buf.write("\2\u0149\u014a\7\u0080\2\2\u014a.\3\2\2\2\u014b\u014c")
        buf.write("\7A\2\2\u014c\60\3\2\2\2\u014d\u014e\7#\2\2\u014e\62\3")
        buf.write("\2\2\2\u014f\u0150\7c\2\2\u0150\u0151\7d\2\2\u0151\u0152")
        buf.write("\7u\2\2\u0152\64\3\2\2\2\u0153\u0154\7c\2\2\u0154\u0155")
        buf.write("\7n\2\2\u0155\u0156\7n\2\2\u0156\66\3\2\2\2\u0157\u0158")
        buf.write("\7c\2\2\u0158\u0159\7p\2\2\u0159\u015a\7{\2\2\u015a8\3")
        buf.write("\2\2\2\u015b\u015c\7d\2\2\u015c\u015d\7k\2\2\u015d\u015e")
        buf.write("\7p\2\2\u015e:\3\2\2\2\u015f\u0160\7e\2\2\u0160\u0161")
        buf.write("\7j\2\2\u0161\u0162\7q\2\2\u0162\u0163\7q\2\2\u0163\u0164")
        buf.write("\7u\2\2\u0164\u0165\7g\2\2\u0165<\3\2\2\2\u0166\u0167")
        buf.write("\7e\2\2\u0167\u0168\7q\2\2\u0168\u0169\7p\2\2\u0169\u016a")
        buf.write("\7v\2\2\u016a\u016b\7g\2\2\u016b\u016c\7z\2\2\u016c\u016d")
        buf.write("\7v\2\2\u016d\u016e\7u\2\2\u016e>\3\2\2\2\u016f\u0170")
        buf.write("\7i\2\2\u0170\u0171\7g\2\2\u0171\u0172\7v\2\2\u0172\u0173")
        buf.write("\7a\2\2\u0173\u0174\7e\2\2\u0174\u0175\7q\2\2\u0175\u0176")
        buf.write("\7p\2\2\u0176\u0177\7v\2\2\u0177\u0178\7g\2\2\u0178\u0179")
        buf.write("\7z\2\2\u0179\u017a\7v\2\2\u017a@\3\2\2\2\u017b\u017c")
        buf.write("\7i\2\2\u017c\u017d\7g\2\2\u017d\u017e\7v\2\2\u017e\u017f")
        buf.write("\7a\2\2\u017f\u0180\7k\2\2\u0180\u0181\7f\2\2\u0181\u0182")
        buf.write("\7g\2\2\u0182\u0183\7p\2\2\u0183\u0184\7v\2\2\u0184B\3")
        buf.write("\2\2\2\u0185\u0186\7j\2\2\u0186\u0187\7c\2\2\u0187\u0188")
        buf.write("\7u\2\2\u0188\u0189\7j\2\2\u0189D\3\2\2\2\u018a\u018b")
        buf.write("\7j\2\2\u018b\u018c\7g\2\2\u018c\u018d\7z\2\2\u018dF\3")
        buf.write("\2\2\2\u018e\u018f\7k\2\2\u018f\u0190\7p\2\2\u0190\u0191")
        buf.write("\7v\2\2\u0191H\3\2\2\2\u0192\u0193\7m\2\2\u0193\u0194")
        buf.write("\7g\2\2\u0194\u0195\7{\2\2\u0195\u0196\7u\2\2\u0196J\3")
        buf.write("\2\2\2\u0197\u0198\7n\2\2\u0198\u0199\7g\2\2\u0199\u019a")
        buf.write("\7p\2\2\u019aL\3\2\2\2\u019b\u019c\7n\2\2\u019c\u019d")
        buf.write("\7k\2\2\u019d\u019e\7u\2\2\u019e\u019f\7v\2\2\u019fN\3")
        buf.write("\2\2\2\u01a0\u01a1\7o\2\2\u01a1\u01a2\7c\2\2\u01a2\u01a3")
        buf.write("\7z\2\2\u01a3P\3\2\2\2\u01a4\u01a5\7o\2\2\u01a5\u01a6")
        buf.write("\7k\2\2\u01a6\u01a7\7p\2\2\u01a7R\3\2\2\2\u01a8\u01a9")
        buf.write("\7q\2\2\u01a9\u01aa\7e\2\2\u01aa\u01ab\7v\2\2\u01abT\3")
        buf.write("\2\2\2\u01ac\u01ad\7t\2\2\u01ad\u01ae\7g\2\2\u01ae\u01af")
        buf.write("\7x\2\2\u01af\u01b0\7g\2\2\u01b0\u01b1\7t\2\2\u01b1\u01b2")
        buf.write("\7u\2\2\u01b2\u01b3\7g\2\2\u01b3\u01b4\7f\2\2\u01b4V\3")
        buf.write("\2\2\2\u01b5\u01b6\7u\2\2\u01b6\u01b7\7g\2\2\u01b7\u01b8")
        buf.write("\7v\2\2\u01b8X\3\2\2\2\u01b9\u01ba\7u\2\2\u01ba\u01bb")
        buf.write("\7q\2\2\u01bb\u01bc\7t\2\2\u01bc\u01bd\7v\2\2\u01bd\u01be")
        buf.write("\7g\2\2\u01be\u01bf\7f\2\2\u01bfZ\3\2\2\2\u01c0\u01c1")
        buf.write("\7u\2\2\u01c1\u01c2\7v\2\2\u01c2\u01c3\7t\2\2\u01c3\\")
        buf.write("\3\2\2\2\u01c4\u01c5\7u\2\2\u01c5\u01c6\7w\2\2\u01c6\u01c7")
        buf.write("\7o\2\2\u01c7^\3\2\2\2\u01c8\u01c9\7v\2\2\u01c9\u01ca")
        buf.write("\7{\2\2\u01ca\u01cb\7r\2\2\u01cb\u01cc\7g\2\2\u01cc`\3")
        buf.write("\2\2\2\u01cd\u01ce\7g\2\2\u01ce\u01cf\7p\2\2\u01cf\u01d0")
        buf.write("\7f\2\2\u01d0b\3\2\2\2\u01d1\u01d2\7c\2\2\u01d2\u01d3")
        buf.write("\7p\2\2\u01d3\u01d4\7f\2\2\u01d4\u01d5\7?\2\2\u01d5d\3")
        buf.write("\2\2\2\u01d6\u01d7\7q\2\2\u01d7\u01d8\7t\2\2\u01d8\u01d9")
        buf.write("\7?\2\2\u01d9f\3\2\2\2\u01da\u01db\7?\2\2\u01db\u01dc")
        buf.write("\7@\2\2\u01dc\u01dd\7?\2\2\u01ddh\3\2\2\2\u01de\u01df")
        buf.write("\7(\2\2\u01df\u01e0\7?\2\2\u01e0j\3\2\2\2\u01e1\u01e2")
        buf.write("\7~\2\2\u01e2\u01e3\7?\2\2\u01e3l\3\2\2\2\u01e4\u01e5")
        buf.write("\7`\2\2\u01e5\u01e6\7?\2\2\u01e6n\3\2\2\2\u01e7\u01e8")
        buf.write("\7/\2\2\u01e8\u01e9\7?\2\2\u01e9p\3\2\2\2\u01ea\u01eb")
        buf.write("\7-\2\2\u01eb\u01ec\7?\2\2\u01ecr\3\2\2\2\u01ed\u01ee")
        buf.write("\7,\2\2\u01ee\u01ef\7?\2\2\u01eft\3\2\2\2\u01f0\u01f1")
        buf.write("\7\61\2\2\u01f1\u01f2\7?\2\2\u01f2v\3\2\2\2\u01f3\u01f4")
        buf.write("\7\61\2\2\u01f4\u01f5\7\61\2\2\u01f5\u01f6\7?\2\2\u01f6")
        buf.write("x\3\2\2\2\u01f7\u01f8\7\'\2\2\u01f8\u01f9\7?\2\2\u01f9")
        buf.write("z\3\2\2\2\u01fa\u01fb\7o\2\2\u01fb\u01fc\7q\2\2\u01fc")
        buf.write("\u01fd\7f\2\2\u01fd\u01fe\7?\2\2\u01fe|\3\2\2\2\u01ff")
        buf.write("\u0200\7,\2\2\u0200\u0201\7,\2\2\u0201\u0202\7?\2\2\u0202")
        buf.write("~\3\2\2\2\u0203\u0204\7@\2\2\u0204\u0205\7@\2\2\u0205")
        buf.write("\u0206\7?\2\2\u0206\u0080\3\2\2\2\u0207\u0208\7>\2\2\u0208")
        buf.write("\u0209\7>\2\2\u0209\u020a\7?\2\2\u020a\u0082\3\2\2\2\u020b")
        buf.write("\u020d\7\17\2\2\u020c\u020b\3\2\2\2\u020c\u020d\3\2\2")
        buf.write("\2\u020d\u020e\3\2\2\2\u020e\u021b\7\f\2\2\u020f\u0211")
        buf.write("\7\"\2\2\u0210\u020f\3\2\2\2\u0211\u0214\3\2\2\2\u0212")
        buf.write("\u0210\3\2\2\2\u0212\u0213\3\2\2\2\u0213\u021c\3\2\2\2")
        buf.write("\u0214\u0212\3\2\2\2\u0215\u0217\7\13\2\2\u0216\u0215")
        buf.write("\3\2\2\2\u0217\u021a\3\2\2\2\u0218\u0216\3\2\2\2\u0218")
        buf.write("\u0219\3\2\2\2\u0219\u021c\3\2\2\2\u021a\u0218\3\2\2\2")
        buf.write("\u021b\u0212\3\2\2\2\u021b\u0218\3\2\2\2\u021c\u021d\3")
        buf.write("\2\2\2\u021d\u021e\bB\2\2\u021e\u0084\3\2\2\2\u021f\u0221")
        buf.write("\7\"\2\2\u0220\u021f\3\2\2\2\u0221\u0222\3\2\2\2\u0222")
        buf.write("\u0220\3\2\2\2\u0222\u0223\3\2\2\2\u0223\u022d\3\2\2\2")
        buf.write("\u0224\u0226\7\13\2\2\u0225\u0224\3\2\2\2\u0226\u0227")
        buf.write("\3\2\2\2\u0227\u0225\3\2\2\2\u0227\u0228\3\2\2\2\u0228")
        buf.write("\u022d\3\2\2\2\u0229\u022a\7^\2\2\u022a\u022d\5\u0083")
        buf.write("B\2\u022b\u022d\5\u0087D\2\u022c\u0220\3\2\2\2\u022c\u0225")
        buf.write("\3\2\2\2\u022c\u0229\3\2\2\2\u022c\u022b\3\2\2\2\u022d")
        buf.write("\u022e\3\2\2\2\u022e\u022f\bC\3\2\u022f\u0086\3\2\2\2")
        buf.write("\u0230\u0234\5\u008bF\2\u0231\u0233\13\2\2\2\u0232\u0231")
        buf.write("\3\2\2\2\u0233\u0236\3\2\2\2\u0234\u0235\3\2\2\2\u0234")
        buf.write("\u0232\3\2\2\2\u0235\u0237\3\2\2\2\u0236\u0234\3\2\2\2")
        buf.write("\u0237\u0238\5\u008dG\2\u0238\u0241\3\2\2\2\u0239\u023d")
        buf.write("\5\u0089E\2\u023a\u023c\n\2\2\2\u023b\u023a\3\2\2\2\u023c")
        buf.write("\u023f\3\2\2\2\u023d\u023b\3\2\2\2\u023d\u023e\3\2\2\2")
        buf.write("\u023e\u0241\3\2\2\2\u023f\u023d\3\2\2\2\u0240\u0230\3")
        buf.write("\2\2\2\u0240\u0239\3\2\2\2\u0241\u0088\3\2\2\2\u0242\u0243")
        buf.write("\7%\2\2\u0243\u008a\3\2\2\2\u0244\u0245\7*\2\2\u0245\u0246")
        buf.write("\7,\2\2\u0246\u008c\3\2\2\2\u0247\u0248\7,\2\2\u0248\u0249")
        buf.write("\7+\2\2\u0249\u008e\3\2\2\2\u024a\u024b\7,\2\2\u024b\u0090")
        buf.write("\3\2\2\2\u024c\u024d\7c\2\2\u024d\u024e\7u\2\2\u024e\u0092")
        buf.write("\3\2\2\2\u024f\u0250\7\60\2\2\u0250\u0094\3\2\2\2\u0251")
        buf.write("\u0252\7k\2\2\u0252\u0253\7o\2\2\u0253\u0254\7r\2\2\u0254")
        buf.write("\u0255\7q\2\2\u0255\u0256\7t\2\2\u0256\u0257\7v\2\2\u0257")
        buf.write("\u0096\3\2\2\2\u0258\u0259\7r\2\2\u0259\u025a\7t\2\2\u025a")
        buf.write("\u025b\7k\2\2\u025b\u025c\7p\2\2\u025c\u025d\7v\2\2\u025d")
        buf.write("\u0098\3\2\2\2\u025e\u025f\7h\2\2\u025f\u0260\7t\2\2\u0260")
        buf.write("\u0261\7q\2\2\u0261\u0262\7o\2\2\u0262\u009a\3\2\2\2\u0263")
        buf.write("\u0264\7\60\2\2\u0264\u0265\7\60\2\2\u0265\u009c\3\2\2")
        buf.write("\2\u0266\u0267\7u\2\2\u0267\u0268\7g\2\2\u0268\u0269\7")
        buf.write("v\2\2\u0269\u026a\7k\2\2\u026a\u026b\7p\2\2\u026b\u026c")
        buf.write("\7v\2\2\u026c\u026d\7n\2\2\u026d\u026e\7g\2\2\u026e\u026f")
        buf.write("\7x\2\2\u026f\u0270\7g\2\2\u0270\u0271\7n\2\2\u0271\u009e")
        buf.write("\3\2\2\2\u0272\u0273\7u\2\2\u0273\u0274\7c\2\2\u0274\u0275")
        buf.write("\7x\2\2\u0275\u0276\7g\2\2\u0276\u00a0\3\2\2\2\u0277\u0278")
        buf.write("\7u\2\2\u0278\u0279\7v\2\2\u0279\u027a\7q\2\2\u027a\u027b")
        buf.write("\7r\2\2\u027b\u00a2\3\2\2\2\u027c\u027d\7n\2\2\u027d\u027e")
        buf.write("\7c\2\2\u027e\u027f\7o\2\2\u027f\u0280\7d\2\2\u0280\u0281")
        buf.write("\7f\2\2\u0281\u0282\7c\2\2\u0282\u00a4\3\2\2\2\u0283\u0284")
        buf.write("\7p\2\2\u0284\u0285\7q\2\2\u0285\u0286\7v\2\2\u0286\u00a6")
        buf.write("\3\2\2\2\u0287\u0288\7.\2\2\u0288\u00a8\3\2\2\2\u0289")
        buf.write("\u028a\7e\2\2\u028a\u028b\7q\2\2\u028b\u028c\7p\2\2\u028c")
        buf.write("\u028d\7u\2\2\u028d\u028e\7v\2\2\u028e\u00aa\3\2\2\2\u028f")
        buf.write("\u0290\7c\2\2\u0290\u0291\7y\2\2\u0291\u0292\7c\2\2\u0292")
        buf.write("\u0293\7k\2\2\u0293\u0294\7v\2\2\u0294\u00ac\3\2\2\2\u0295")
        buf.write("\u0296\7c\2\2\u0296\u0297\7u\2\2\u0297\u0298\7u\2\2\u0298")
        buf.write("\u0299\7g\2\2\u0299\u029a\7t\2\2\u029a\u029b\7v\2\2\u029b")
        buf.write("\u00ae\3\2\2\2\u029c\u029d\7x\2\2\u029d\u029e\7c\2\2\u029e")
        buf.write("\u029f\7t\2\2\u029f\u00b0\3\2\2\2\u02a0\u02a1\7v\2\2\u02a1")
        buf.write("\u02a2\7t\2\2\u02a2\u02a3\7c\2\2\u02a3\u02a4\7r\2\2\u02a4")
        buf.write("\u00b2\3\2\2\2\u02a5\u02a6\7r\2\2\u02a6\u02a7\7c\2\2\u02a7")
        buf.write("\u02a8\7u\2\2\u02a8\u02a9\7u\2\2\u02a9\u00b4\3\2\2\2\u02aa")
        buf.write("\u02ab\7f\2\2\u02ab\u02ac\7g\2\2\u02ac\u02ad\7n\2\2\u02ad")
        buf.write("\u00b6\3\2\2\2\u02ae\u02af\7u\2\2\u02af\u02b0\7r\2\2\u02b0")
        buf.write("\u02b1\7c\2\2\u02b1\u02b2\7y\2\2\u02b2\u02b3\7p\2\2\u02b3")
        buf.write("\u00b8\3\2\2\2\u02b4\u02b5\7h\2\2\u02b5\u02b6\7k\2\2\u02b6")
        buf.write("\u02b7\7p\2\2\u02b7\u02b8\7c\2\2\u02b8\u02b9\7n\2\2\u02b9")
        buf.write("\u02ba\7n\2\2\u02ba\u02bb\7{\2\2\u02bb\u00ba\3\2\2\2\u02bc")
        buf.write("\u02bd\7k\2\2\u02bd\u02be\7p\2\2\u02be\u02bf\7x\2\2\u02bf")
        buf.write("\u02c0\7c\2\2\u02c0\u02c1\7t\2\2\u02c1\u02c2\7k\2\2\u02c2")
        buf.write("\u02c3\7c\2\2\u02c3\u02c4\7p\2\2\u02c4\u02c5\7v\2\2\u02c5")
        buf.write("\u00bc\3\2\2\2\u02c6\u02c7\7i\2\2\u02c7\u02c8\7q\2\2\u02c8")
        buf.write("\u00be\3\2\2\2\u02c9\u02ca\7d\2\2\u02ca\u02cb\7w\2\2\u02cb")
        buf.write("\u02cc\7k\2\2\u02cc\u02cd\7n\2\2\u02cd\u02ce\7v\2\2\u02ce")
        buf.write("\u02cf\7k\2\2\u02cf\u02d0\7p\2\2\u02d0\u00c0\3\2\2\2\u02d1")
        buf.write("\u02d2\7u\2\2\u02d2\u02d3\7g\2\2\u02d3\u02d4\7s\2\2\u02d4")
        buf.write("\u02d5\7w\2\2\u02d5\u02d6\7g\2\2\u02d6\u02d7\7p\2\2\u02d7")
        buf.write("\u02d8\7v\2\2\u02d8\u02d9\7k\2\2\u02d9\u02da\7c\2\2\u02da")
        buf.write("\u02db\7n\2\2\u02db\u00c2\3\2\2\2\u02dc\u02dd\7y\2\2\u02dd")
        buf.write("\u02de\7j\2\2\u02de\u02df\7g\2\2\u02df\u02e0\7p\2\2\u02e0")
        buf.write("\u00c4\3\2\2\2\u02e1\u02e2\7n\2\2\u02e2\u02e3\7g\2\2\u02e3")
        buf.write("\u02e4\7v\2\2\u02e4\u00c6\3\2\2\2\u02e5\u02e6\7k\2\2\u02e6")
        buf.write("\u02e7\7h\2\2\u02e7\u00c8\3\2\2\2\u02e8\u02e9\7g\2\2\u02e9")
        buf.write("\u02ea\7n\2\2\u02ea\u02eb\7k\2\2\u02eb\u02ec\7h\2\2\u02ec")
        buf.write("\u00ca\3\2\2\2\u02ed\u02ee\7g\2\2\u02ee\u02ef\7n\2\2\u02ef")
        buf.write("\u02f0\7u\2\2\u02f0\u02f1\7g\2\2\u02f1\u00cc\3\2\2\2\u02f2")
        buf.write("\u02f3\7B\2\2\u02f3\u00ce\3\2\2\2\u02f4\u02f5\7y\2\2\u02f5")
        buf.write("\u02f6\7j\2\2\u02f6\u02f7\7k\2\2\u02f7\u02f8\7n\2\2\u02f8")
        buf.write("\u02f9\7g\2\2\u02f9\u00d0\3\2\2\2\u02fa\u02fb\7i\2\2\u02fb")
        buf.write("\u02fc\7n\2\2\u02fc\u02fd\7q\2\2\u02fd\u02fe\7d\2\2\u02fe")
        buf.write("\u02ff\7c\2\2\u02ff\u0300\7n\2\2\u0300\u00d2\3\2\2\2\u0301")
        buf.write("\u0302\7f\2\2\u0302\u0303\7g\2\2\u0303\u0304\7h\2\2\u0304")
        buf.write("\u00d4\3\2\2\2\u0305\u0306\7t\2\2\u0306\u0307\7g\2\2\u0307")
        buf.write("\u0308\7v\2\2\u0308\u0309\7w\2\2\u0309\u030a\7t\2\2\u030a")
        buf.write("\u030b\7p\2\2\u030b\u030c\7u\2\2\u030c\u00d6\3\2\2\2\u030d")
        buf.write("\u030e\7g\2\2\u030e\u030f\7z\2\2\u030f\u0310\7k\2\2\u0310")
        buf.write("\u0311\7u\2\2\u0311\u0312\7v\2\2\u0312\u0313\7u\2\2\u0313")
        buf.write("\u00d8\3\2\2\2\u0314\u0315\7y\2\2\u0315\u0316\7j\2\2\u0316")
        buf.write("\u0317\7g\2\2\u0317\u0318\7t\2\2\u0318\u0319\7g\2\2\u0319")
        buf.write("\u00da\3\2\2\2\u031a\u031b\7?\2\2\u031b\u00dc\3\2\2\2")
        buf.write("\u031c\u031d\7h\2\2\u031d\u031e\7q\2\2\u031e\u031f\7t")
        buf.write("\2\2\u031f\u0320\3\2\2\2\u0320\u0321\bo\4\2\u0321\u00de")
        buf.write("\3\2\2\2\u0322\u0323\7k\2\2\u0323\u0324\7p\2\2\u0324\u0325")
        buf.write("\3\2\2\2\u0325\u0326\bp\5\2\u0326\u00e0\3\2\2\2\u0327")
        buf.write("\u0328\7<\2\2\u0328\u00e2\3\2\2\2\u0329\u032a\7P\2\2\u032a")
        buf.write("\u032b\7q\2\2\u032b\u032c\7p\2\2\u032c\u032d\7g\2\2\u032d")
        buf.write("\u00e4\3\2\2\2\u032e\u032f\7c\2\2\u032f\u0330\7v\2\2\u0330")
        buf.write("\u0331\7q\2\2\u0331\u0332\7o\2\2\u0332\u0333\7k\2\2\u0333")
        buf.write("\u0334\7e\2\2\u0334\u0335\7c\2\2\u0335\u0336\7n\2\2\u0336")
        buf.write("\u0337\7n\2\2\u0337\u0338\7{\2\2\u0338\u00e6\3\2\2\2\u0339")
        buf.write("\u033a\7H\2\2\u033a\u033b\7c\2\2\u033b\u033c\7n\2\2\u033c")
        buf.write("\u033d\7u\2\2\u033d\u0343\7g\2\2\u033e\u033f\7V\2\2\u033f")
        buf.write("\u0340\7t\2\2\u0340\u0341\7w\2\2\u0341\u0343\7g\2\2\u0342")
        buf.write("\u0339\3\2\2\2\u0342\u033e\3\2\2\2\u0343\u00e8\3\2\2\2")
        buf.write("\u0344\u0345\7g\2\2\u0345\u0346\7v\2\2\u0346\u0347\7g")
        buf.write("\2\2\u0347\u0348\7t\2\2\u0348\u0349\7p\2\2\u0349\u034a")
        buf.write("\7c\2\2\u034a\u034b\7n\2\2\u034b\u00ea\3\2\2\2\u034c\u034e")
        buf.write("\t\3\2\2\u034d\u034c\3\2\2\2\u034e\u034f\3\2\2\2\u034f")
        buf.write("\u034d\3\2\2\2\u034f\u0350\3\2\2\2\u0350\u036a\3\2\2\2")
        buf.write("\u0351\u0352\7\62\2\2\u0352\u0353\7z\2\2\u0353\u0355\3")
        buf.write("\2\2\2\u0354\u0356\t\4\2\2\u0355\u0354\3\2\2\2\u0356\u0357")
        buf.write("\3\2\2\2\u0357\u0355\3\2\2\2\u0357\u0358\3\2\2\2\u0358")
        buf.write("\u036a\3\2\2\2\u0359\u035a\7\62\2\2\u035a\u035b\7d\2\2")
        buf.write("\u035b\u035d\3\2\2\2\u035c\u035e\t\5\2\2\u035d\u035c\3")
        buf.write("\2\2\2\u035e\u035f\3\2\2\2\u035f\u035d\3\2\2\2\u035f\u0360")
        buf.write("\3\2\2\2\u0360\u036a\3\2\2\2\u0361\u0362\7\62\2\2\u0362")
        buf.write("\u0363\7q\2\2\u0363\u0365\3\2\2\2\u0364\u0366\t\6\2\2")
        buf.write("\u0365\u0364\3\2\2\2\u0366\u0367\3\2\2\2\u0367\u0365\3")
        buf.write("\2\2\2\u0367\u0368\3\2\2\2\u0368\u036a\3\2\2\2\u0369\u034d")
        buf.write("\3\2\2\2\u0369\u0351\3\2\2\2\u0369\u0359\3\2\2\2\u0369")
        buf.write("\u0361\3\2\2\2\u036a\u00ec\3\2\2\2\u036b\u036f\t\7\2\2")
        buf.write("\u036c\u036e\t\b\2\2\u036d\u036c\3\2\2\2\u036e\u0371\3")
        buf.write("\2\2\2\u036f\u036d\3\2\2\2\u036f\u0370\3\2\2\2\u0370\u00ee")
        buf.write("\3\2\2\2\u0371\u036f\3\2\2\2\u0372\u0375\t\t\2\2\u0373")
        buf.write("\u0376\5\u00f3z\2\u0374\u0376\5\u00edw\2\u0375\u0373\3")
        buf.write("\2\2\2\u0375\u0374\3\2\2\2\u0376\u00f0\3\2\2\2\u0377\u0378")
        buf.write("\7/\2\2\u0378\u0379\7@\2\2\u0379\u037d\3\2\2\2\u037a\u037c")
        buf.write("\7\"\2\2\u037b\u037a\3\2\2\2\u037c\u037f\3\2\2\2\u037d")
        buf.write("\u037b\3\2\2\2\u037d\u037e\3\2\2\2\u037e\u0380\3\2\2\2")
        buf.write("\u037f\u037d\3\2\2\2\u0380\u0381\5\u00edw\2\u0381\u00f2")
        buf.write("\3\2\2\2\u0382\u0383\7\62\2\2\u0383\u0384\7Z\2\2\u0384")
        buf.write("\u0386\3\2\2\2\u0385\u0387\5\u00f5{\2\u0386\u0385\3\2")
        buf.write("\2\2\u0387\u0388\3\2\2\2\u0388\u0386\3\2\2\2\u0388\u0389")
        buf.write("\3\2\2\2\u0389\u00f4\3\2\2\2\u038a\u038b\t\4\2\2\u038b")
        buf.write("\u00f6\3\2\2\2\u038c\u038d\7]\2\2\u038d\u038e\b|\6\2\u038e")
        buf.write("\u00f8\3\2\2\2\u038f\u0390\7_\2\2\u0390\u0391\b}\7\2\u0391")
        buf.write("\u00fa\3\2\2\2\u0392\u0393\7}\2\2\u0393\u0394\b~\b\2\u0394")
        buf.write("\u00fc\3\2\2\2\u0395\u0396\7\177\2\2\u0396\u0397\b\177")
        buf.write("\t\2\u0397\u00fe\3\2\2\2\u0398\u0399\7*\2\2\u0399\u039a")
        buf.write("\b\u0080\n\2\u039a\u0100\3\2\2\2\u039b\u039c\7+\2\2\u039c")
        buf.write("\u039d\b\u0081\13\2\u039d\u0102\3\2\2\2\u039e\u039f\7")
        buf.write("=\2\2\u039f\u0104\3\2\2\2\u03a0\u03a3\5\u0107\u0084\2")
        buf.write("\u03a1\u03a3\5\u0109\u0085\2\u03a2\u03a0\3\2\2\2\u03a2")
        buf.write("\u03a1\3\2\2\2\u03a3\u0106\3\2\2\2\u03a4\u03a9\7)\2\2")
        buf.write("\u03a5\u03a8\5\u010f\u0088\2\u03a6\u03a8\n\n\2\2\u03a7")
        buf.write("\u03a5\3\2\2\2\u03a7\u03a6\3\2\2\2\u03a8\u03ab\3\2\2\2")
        buf.write("\u03a9\u03a7\3\2\2\2\u03a9\u03aa\3\2\2\2\u03aa\u03ac\3")
        buf.write("\2\2\2\u03ab\u03a9\3\2\2\2\u03ac\u03b7\7)\2\2\u03ad\u03b2")
        buf.write("\7$\2\2\u03ae\u03b1\5\u010f\u0088\2\u03af\u03b1\n\13\2")
        buf.write("\2\u03b0\u03ae\3\2\2\2\u03b0\u03af\3\2\2\2\u03b1\u03b4")
        buf.write("\3\2\2\2\u03b2\u03b0\3\2\2\2\u03b2\u03b3\3\2\2\2\u03b3")
        buf.write("\u03b5\3\2\2\2\u03b4\u03b2\3\2\2\2\u03b5\u03b7\7$\2\2")
        buf.write("\u03b6\u03a4\3\2\2\2\u03b6\u03ad\3\2\2\2\u03b7\u0108\3")
        buf.write("\2\2\2\u03b8\u03b9\7)\2\2\u03b9\u03ba\7)\2\2\u03ba\u03bb")
        buf.write("\7)\2\2\u03bb\u03bf\3\2\2\2\u03bc\u03be\5\u010b\u0086")
        buf.write("\2\u03bd\u03bc\3\2\2\2\u03be\u03c1\3\2\2\2\u03bf\u03c0")
        buf.write("\3\2\2\2\u03bf\u03bd\3\2\2\2\u03c0\u03c2\3\2\2\2\u03c1")
        buf.write("\u03bf\3\2\2\2\u03c2\u03c3\7)\2\2\u03c3\u03c4\7)\2\2\u03c4")
        buf.write("\u03d3\7)\2\2\u03c5\u03c6\7$\2\2\u03c6\u03c7\7$\2\2\u03c7")
        buf.write("\u03c8\7$\2\2\u03c8\u03cc\3\2\2\2\u03c9\u03cb\5\u010b")
        buf.write("\u0086\2\u03ca\u03c9\3\2\2\2\u03cb\u03ce\3\2\2\2\u03cc")
        buf.write("\u03cd\3\2\2\2\u03cc\u03ca\3\2\2\2\u03cd\u03cf\3\2\2\2")
        buf.write("\u03ce\u03cc\3\2\2\2\u03cf\u03d0\7$\2\2\u03d0\u03d1\7")
        buf.write("$\2\2\u03d1\u03d3\7$\2\2\u03d2\u03b8\3\2\2\2\u03d2\u03c5")
        buf.write("\3\2\2\2\u03d3\u010a\3\2\2\2\u03d4\u03d7\5\u010d\u0087")
        buf.write("\2\u03d5\u03d7\5\u010f\u0088\2\u03d6\u03d4\3\2\2\2\u03d6")
        buf.write("\u03d5\3\2\2\2\u03d7\u010c\3\2\2\2\u03d8\u03d9\n\f\2\2")
        buf.write("\u03d9\u010e\3\2\2\2\u03da\u03db\7^\2\2\u03db\u03df\13")
        buf.write("\2\2\2\u03dc\u03dd\7^\2\2\u03dd\u03df\5\u0083B\2\u03de")
        buf.write("\u03da\3\2\2\2\u03de\u03dc\3\2\2\2\u03df\u0110\3\2\2\2")
        buf.write("\"\2\u020c\u0212\u0218\u021b\u0222\u0227\u022c\u0234\u023d")
        buf.write("\u0240\u0342\u034f\u0357\u035f\u0367\u0369\u036f\u0375")
        buf.write("\u037d\u0388\u03a2\u03a7\u03a9\u03b0\u03b2\u03b6\u03bf")
        buf.write("\u03cc\u03d2\u03d6\u03de\f\3B\2\b\2\2\3o\3\3p\4\3|\5\3")
        buf.write("}\6\3~\7\3\177\b\3\u0080\t\3\u0081\n")
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
    T__63 = 64
    NL = 65
    WS = 66
    COMMENT_START = 67
    OPEN_MULTI_COMMENT = 68
    CLOSE_MULTI_COMMENT = 69
    STAR = 70
    AS = 71
    DOT = 72
    IMPORT = 73
    PRINT = 74
    FROM = 75
    RANGE = 76
    SETINTLEVEL = 77
    SAVE = 78
    STOP = 79
    LAMBDA = 80
    NOT = 81
    COMMA = 82
    CONST = 83
    AWAIT = 84
    ASSERT = 85
    VAR = 86
    TRAP = 87
    PASS = 88
    DEL = 89
    SPAWN = 90
    FINALLY = 91
    INVARIANT = 92
    GO = 93
    BUILTIN = 94
    SEQUENTIAL = 95
    WHEN = 96
    LET = 97
    IF = 98
    ELIF = 99
    ELSE = 100
    AT = 101
    WHILE = 102
    GLOBAL = 103
    DEF = 104
    RETURNS = 105
    EXISTS = 106
    WHERE = 107
    EQ = 108
    FOR = 109
    IN = 110
    COLON = 111
    NONE = 112
    ATOMICALLY = 113
    BOOL = 114
    ETERNAL = 115
    INT = 116
    NAME = 117
    ATOM = 118
    ARROWID = 119
    HEX_INTEGER = 120
    OPEN_BRACK = 121
    CLOSE_BRACK = 122
    OPEN_BRACES = 123
    CLOSE_BRACES = 124
    OPEN_PAREN = 125
    CLOSE_PAREN = 126
    SEMI_COLON = 127
    STRING = 128

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'or'", "'&'", "'|'", "'^'", "'-'", "'+'", "'//'", 
            "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", "'!='", 
            "'<'", "'<='", "'>'", "'>='", "'=>'", "'~'", "'?'", "'!'", "'abs'", 
            "'all'", "'any'", "'bin'", "'choose'", "'contexts'", "'get_context'", 
            "'get_ident'", "'hash'", "'hex'", "'int'", "'keys'", "'len'", 
            "'list'", "'max'", "'min'", "'oct'", "'reversed'", "'set'", 
            "'sorted'", "'str'", "'sum'", "'type'", "'end'", "'and='", "'or='", 
            "'=>='", "'&='", "'|='", "'^='", "'-='", "'+='", "'*='", "'/='", 
            "'//='", "'%='", "'mod='", "'**='", "'>>='", "'<<='", "'#'", 
            "'(*'", "'*)'", "'*'", "'as'", "'.'", "'import'", "'print'", 
            "'from'", "'..'", "'setintlevel'", "'save'", "'stop'", "'lambda'", 
            "'not'", "','", "'const'", "'await'", "'assert'", "'var'", "'trap'", 
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
                  "T__62", "T__63", "NL", "WS", "COMMENT", "COMMENT_START", 
                  "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", "STAR", "AS", 
                  "DOT", "IMPORT", "PRINT", "FROM", "RANGE", "SETINTLEVEL", 
                  "SAVE", "STOP", "LAMBDA", "NOT", "COMMA", "CONST", "AWAIT", 
                  "ASSERT", "VAR", "TRAP", "PASS", "DEL", "SPAWN", "FINALLY", 
                  "INVARIANT", "GO", "BUILTIN", "SEQUENTIAL", "WHEN", "LET", 
                  "IF", "ELIF", "ELSE", "AT", "WHILE", "GLOBAL", "DEF", 
                  "RETURNS", "EXISTS", "WHERE", "EQ", "FOR", "IN", "COLON", 
                  "NONE", "ATOMICALLY", "BOOL", "ETERNAL", "INT", "NAME", 
                  "ATOM", "ARROWID", "HEX_INTEGER", "HEX_DIGIT", "OPEN_BRACK", 
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
            actions[64] = self.NL_action 
            actions[109] = self.FOR_action 
            actions[110] = self.IN_action 
            actions[122] = self.OPEN_BRACK_action 
            actions[123] = self.CLOSE_BRACK_action 
            actions[124] = self.OPEN_BRACES_action 
            actions[125] = self.CLOSE_BRACES_action 
            actions[126] = self.OPEN_PAREN_action 
            actions[127] = self.CLOSE_PAREN_action 
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
     


