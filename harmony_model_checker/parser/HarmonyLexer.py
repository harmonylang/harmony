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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\u0080")
        buf.write("\u03d4\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("\4\u0084\t\u0084\4\u0085\t\u0085\4\u0086\t\u0086\3\2\3")
        buf.write("\2\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7")
        buf.write("\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\f\3\f")
        buf.write("\3\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3\17\3\20\3\20\3")
        buf.write("\20\3\21\3\21\3\21\3\22\3\22\3\23\3\23\3\23\3\24\3\24")
        buf.write("\3\25\3\25\3\25\3\26\3\26\3\26\3\27\3\27\3\30\3\30\3\31")
        buf.write("\3\31\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\34\3\34")
        buf.write("\3\34\3\34\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37")
        buf.write("\3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3 \3!\3!\3!\3!\3!\3")
        buf.write("!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3\"\3#\3#\3#\3#\3$\3$\3")
        buf.write("$\3$\3$\3%\3%\3%\3%\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3(")
        buf.write("\3(\3(\3(\3)\3)\3)\3)\3)\3)\3)\3)\3)\3*\3*\3*\3*\3+\3")
        buf.write("+\3+\3+\3+\3+\3+\3,\3,\3,\3,\3-\3-\3-\3-\3.\3.\3.\3.\3")
        buf.write(".\3/\3/\3/\3/\3\60\3\60\3\60\3\60\3\60\3\61\3\61\3\61")
        buf.write("\3\61\3\62\3\62\3\62\3\62\3\63\3\63\3\63\3\64\3\64\3\64")
        buf.write("\3\65\3\65\3\65\3\66\3\66\3\66\3\67\3\67\3\67\38\38\3")
        buf.write("8\39\39\39\3:\3:\3:\3:\3;\3;\3;\3<\3<\3<\3<\3<\3=\3=\3")
        buf.write("=\3=\3>\3>\3>\3>\3?\3?\3?\3?\3@\5@\u0201\n@\3@\3@\7@\u0205")
        buf.write("\n@\f@\16@\u0208\13@\3@\7@\u020b\n@\f@\16@\u020e\13@\5")
        buf.write("@\u0210\n@\3@\3@\3A\6A\u0215\nA\rA\16A\u0216\3A\6A\u021a")
        buf.write("\nA\rA\16A\u021b\3A\3A\3A\5A\u0221\nA\3A\3A\3B\3B\7B\u0227")
        buf.write("\nB\fB\16B\u022a\13B\3B\3B\3B\3B\7B\u0230\nB\fB\16B\u0233")
        buf.write("\13B\5B\u0235\nB\3C\3C\3D\3D\3D\3E\3E\3E\3F\3F\3G\3G\3")
        buf.write("G\3H\3H\3I\3I\3I\3I\3I\3I\3I\3J\3J\3J\3J\3J\3J\3K\3K\3")
        buf.write("K\3K\3K\3L\3L\3L\3M\3M\3M\3M\3M\3M\3M\3M\3M\3M\3M\3M\3")
        buf.write("N\3N\3N\3N\3N\3O\3O\3O\3O\3O\3P\3P\3P\3P\3P\3P\3P\3Q\3")
        buf.write("Q\3Q\3Q\3R\3R\3S\3S\3S\3S\3S\3S\3T\3T\3T\3T\3T\3T\3U\3")
        buf.write("U\3U\3U\3U\3U\3U\3V\3V\3V\3V\3W\3W\3W\3W\3W\3X\3X\3X\3")
        buf.write("X\3X\3Y\3Y\3Y\3Y\3Z\3Z\3Z\3Z\3Z\3Z\3[\3[\3[\3[\3[\3[\3")
        buf.write("[\3[\3\\\3\\\3\\\3\\\3\\\3\\\3\\\3\\\3\\\3\\\3]\3]\3]")
        buf.write("\3^\3^\3^\3^\3^\3^\3^\3^\3_\3_\3_\3_\3_\3_\3_\3_\3_\3")
        buf.write("_\3_\3`\3`\3`\3`\3`\3a\3a\3a\3a\3b\3b\3b\3c\3c\3c\3c\3")
        buf.write("c\3d\3d\3d\3d\3d\3e\3e\3f\3f\3f\3f\3f\3f\3g\3g\3g\3g\3")
        buf.write("g\3g\3g\3h\3h\3h\3h\3i\3i\3i\3i\3i\3i\3i\3i\3j\3j\3j\3")
        buf.write("j\3j\3j\3j\3k\3k\3k\3k\3k\3k\3l\3l\3m\3m\3m\3m\3m\3m\3")
        buf.write("n\3n\3n\3n\3n\3o\3o\3p\3p\3p\3p\3p\3q\3q\3q\3q\3q\3q\3")
        buf.write("q\3q\3q\3q\3q\3r\3r\3r\3r\3r\3r\3r\3r\3r\5r\u0337\nr\3")
        buf.write("s\3s\3s\3s\3s\3s\3s\3s\3t\6t\u0342\nt\rt\16t\u0343\3t")
        buf.write("\3t\3t\3t\6t\u034a\nt\rt\16t\u034b\3t\3t\3t\3t\6t\u0352")
        buf.write("\nt\rt\16t\u0353\3t\3t\3t\3t\6t\u035a\nt\rt\16t\u035b")
        buf.write("\5t\u035e\nt\3u\3u\7u\u0362\nu\fu\16u\u0365\13u\3v\3v")
        buf.write("\3v\5v\u036a\nv\3w\3w\3w\3w\7w\u0370\nw\fw\16w\u0373\13")
        buf.write("w\3w\3w\3x\3x\3x\3x\6x\u037b\nx\rx\16x\u037c\3y\3y\3z")
        buf.write("\3z\3z\3{\3{\3{\3|\3|\3|\3}\3}\3}\3~\3~\3~\3\177\3\177")
        buf.write("\3\177\3\u0080\3\u0080\3\u0081\3\u0081\5\u0081\u0397\n")
        buf.write("\u0081\3\u0082\3\u0082\3\u0082\7\u0082\u039c\n\u0082\f")
        buf.write("\u0082\16\u0082\u039f\13\u0082\3\u0082\3\u0082\3\u0082")
        buf.write("\3\u0082\7\u0082\u03a5\n\u0082\f\u0082\16\u0082\u03a8")
        buf.write("\13\u0082\3\u0082\5\u0082\u03ab\n\u0082\3\u0083\3\u0083")
        buf.write("\3\u0083\3\u0083\3\u0083\7\u0083\u03b2\n\u0083\f\u0083")
        buf.write("\16\u0083\u03b5\13\u0083\3\u0083\3\u0083\3\u0083\3\u0083")
        buf.write("\3\u0083\3\u0083\3\u0083\3\u0083\7\u0083\u03bf\n\u0083")
        buf.write("\f\u0083\16\u0083\u03c2\13\u0083\3\u0083\3\u0083\3\u0083")
        buf.write("\5\u0083\u03c7\n\u0083\3\u0084\3\u0084\5\u0084\u03cb\n")
        buf.write("\u0084\3\u0085\3\u0085\3\u0086\3\u0086\3\u0086\3\u0086")
        buf.write("\5\u0086\u03d3\n\u0086\5\u0228\u03b3\u03c0\2\u0087\3\3")
        buf.write("\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16")
        buf.write("\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61")
        buf.write("\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*")
        buf.write("S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q:s;u<w")
        buf.write("=y>{?}@\177A\u0081B\u0083\2\u0085C\u0087D\u0089E\u008b")
        buf.write("F\u008dG\u008fH\u0091I\u0093J\u0095K\u0097L\u0099M\u009b")
        buf.write("N\u009dO\u009fP\u00a1Q\u00a3R\u00a5S\u00a7T\u00a9U\u00ab")
        buf.write("V\u00adW\u00afX\u00b1Y\u00b3Z\u00b5[\u00b7\\\u00b9]\u00bb")
        buf.write("^\u00bd_\u00bf`\u00c1a\u00c3b\u00c5c\u00c7d\u00c9e\u00cb")
        buf.write("f\u00cdg\u00cfh\u00d1i\u00d3j\u00d5k\u00d7l\u00d9m\u00db")
        buf.write("n\u00ddo\u00dfp\u00e1q\u00e3r\u00e5s\u00e7t\u00e9u\u00eb")
        buf.write("v\u00edw\u00efx\u00f1\2\u00f3y\u00f5z\u00f7{\u00f9|\u00fb")
        buf.write("}\u00fd~\u00ff\177\u0101\u0080\u0103\2\u0105\2\u0107\2")
        buf.write("\u0109\2\u010b\2\3\2\r\4\2\f\f\16\17\3\2\62;\5\2\62;C")
        buf.write("Hch\3\2\62\63\3\2\629\5\2C\\aac|\6\2\62;C\\aac|\3\2\60")
        buf.write("\60\6\2\f\f\16\17))^^\6\2\f\f\16\17$$^^\3\2^^\2\u03ef")
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
        buf.write("{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0085")
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
        buf.write("\3\2\2\2\2\u00db\3\2\2\2\2\u00dd\3\2\2\2\2\u00df\3\2\2")
        buf.write("\2\2\u00e1\3\2\2\2\2\u00e3\3\2\2\2\2\u00e5\3\2\2\2\2\u00e7")
        buf.write("\3\2\2\2\2\u00e9\3\2\2\2\2\u00eb\3\2\2\2\2\u00ed\3\2\2")
        buf.write("\2\2\u00ef\3\2\2\2\2\u00f3\3\2\2\2\2\u00f5\3\2\2\2\2\u00f7")
        buf.write("\3\2\2\2\2\u00f9\3\2\2\2\2\u00fb\3\2\2\2\2\u00fd\3\2\2")
        buf.write("\2\2\u00ff\3\2\2\2\2\u0101\3\2\2\2\3\u010d\3\2\2\2\5\u0111")
        buf.write("\3\2\2\2\7\u0114\3\2\2\2\t\u0116\3\2\2\2\13\u0118\3\2")
        buf.write("\2\2\r\u011a\3\2\2\2\17\u011c\3\2\2\2\21\u011e\3\2\2\2")
        buf.write("\23\u0121\3\2\2\2\25\u0123\3\2\2\2\27\u0125\3\2\2\2\31")
        buf.write("\u0129\3\2\2\2\33\u012c\3\2\2\2\35\u012f\3\2\2\2\37\u0132")
        buf.write("\3\2\2\2!\u0135\3\2\2\2#\u0138\3\2\2\2%\u013a\3\2\2\2")
        buf.write("\'\u013d\3\2\2\2)\u013f\3\2\2\2+\u0142\3\2\2\2-\u0145")
        buf.write("\3\2\2\2/\u0147\3\2\2\2\61\u0149\3\2\2\2\63\u014b\3\2")
        buf.write("\2\2\65\u014f\3\2\2\2\67\u0153\3\2\2\29\u0157\3\2\2\2")
        buf.write(";\u015b\3\2\2\2=\u0162\3\2\2\2?\u016b\3\2\2\2A\u0177\3")
        buf.write("\2\2\2C\u0181\3\2\2\2E\u0186\3\2\2\2G\u018a\3\2\2\2I\u018f")
        buf.write("\3\2\2\2K\u0193\3\2\2\2M\u0198\3\2\2\2O\u019c\3\2\2\2")
        buf.write("Q\u01a0\3\2\2\2S\u01a9\3\2\2\2U\u01ad\3\2\2\2W\u01b4\3")
        buf.write("\2\2\2Y\u01b8\3\2\2\2[\u01bc\3\2\2\2]\u01c1\3\2\2\2_\u01c5")
        buf.write("\3\2\2\2a\u01ca\3\2\2\2c\u01ce\3\2\2\2e\u01d2\3\2\2\2")
        buf.write("g\u01d5\3\2\2\2i\u01d8\3\2\2\2k\u01db\3\2\2\2m\u01de\3")
        buf.write("\2\2\2o\u01e1\3\2\2\2q\u01e4\3\2\2\2s\u01e7\3\2\2\2u\u01eb")
        buf.write("\3\2\2\2w\u01ee\3\2\2\2y\u01f3\3\2\2\2{\u01f7\3\2\2\2")
        buf.write("}\u01fb\3\2\2\2\177\u0200\3\2\2\2\u0081\u0220\3\2\2\2")
        buf.write("\u0083\u0234\3\2\2\2\u0085\u0236\3\2\2\2\u0087\u0238\3")
        buf.write("\2\2\2\u0089\u023b\3\2\2\2\u008b\u023e\3\2\2\2\u008d\u0240")
        buf.write("\3\2\2\2\u008f\u0243\3\2\2\2\u0091\u0245\3\2\2\2\u0093")
        buf.write("\u024c\3\2\2\2\u0095\u0252\3\2\2\2\u0097\u0257\3\2\2\2")
        buf.write("\u0099\u025a\3\2\2\2\u009b\u0266\3\2\2\2\u009d\u026b\3")
        buf.write("\2\2\2\u009f\u0270\3\2\2\2\u00a1\u0277\3\2\2\2\u00a3\u027b")
        buf.write("\3\2\2\2\u00a5\u027d\3\2\2\2\u00a7\u0283\3\2\2\2\u00a9")
        buf.write("\u0289\3\2\2\2\u00ab\u0290\3\2\2\2\u00ad\u0294\3\2\2\2")
        buf.write("\u00af\u0299\3\2\2\2\u00b1\u029e\3\2\2\2\u00b3\u02a2\3")
        buf.write("\2\2\2\u00b5\u02a8\3\2\2\2\u00b7\u02b0\3\2\2\2\u00b9\u02ba")
        buf.write("\3\2\2\2\u00bb\u02bd\3\2\2\2\u00bd\u02c5\3\2\2\2\u00bf")
        buf.write("\u02d0\3\2\2\2\u00c1\u02d5\3\2\2\2\u00c3\u02d9\3\2\2\2")
        buf.write("\u00c5\u02dc\3\2\2\2\u00c7\u02e1\3\2\2\2\u00c9\u02e6\3")
        buf.write("\2\2\2\u00cb\u02e8\3\2\2\2\u00cd\u02ee\3\2\2\2\u00cf\u02f5")
        buf.write("\3\2\2\2\u00d1\u02f9\3\2\2\2\u00d3\u0301\3\2\2\2\u00d5")
        buf.write("\u0308\3\2\2\2\u00d7\u030e\3\2\2\2\u00d9\u0310\3\2\2\2")
        buf.write("\u00db\u0316\3\2\2\2\u00dd\u031b\3\2\2\2\u00df\u031d\3")
        buf.write("\2\2\2\u00e1\u0322\3\2\2\2\u00e3\u0336\3\2\2\2\u00e5\u0338")
        buf.write("\3\2\2\2\u00e7\u035d\3\2\2\2\u00e9\u035f\3\2\2\2\u00eb")
        buf.write("\u0366\3\2\2\2\u00ed\u036b\3\2\2\2\u00ef\u0376\3\2\2\2")
        buf.write("\u00f1\u037e\3\2\2\2\u00f3\u0380\3\2\2\2\u00f5\u0383\3")
        buf.write("\2\2\2\u00f7\u0386\3\2\2\2\u00f9\u0389\3\2\2\2\u00fb\u038c")
        buf.write("\3\2\2\2\u00fd\u038f\3\2\2\2\u00ff\u0392\3\2\2\2\u0101")
        buf.write("\u0396\3\2\2\2\u0103\u03aa\3\2\2\2\u0105\u03c6\3\2\2\2")
        buf.write("\u0107\u03ca\3\2\2\2\u0109\u03cc\3\2\2\2\u010b\u03d2\3")
        buf.write("\2\2\2\u010d\u010e\7c\2\2\u010e\u010f\7p\2\2\u010f\u0110")
        buf.write("\7f\2\2\u0110\4\3\2\2\2\u0111\u0112\7q\2\2\u0112\u0113")
        buf.write("\7t\2\2\u0113\6\3\2\2\2\u0114\u0115\7(\2\2\u0115\b\3\2")
        buf.write("\2\2\u0116\u0117\7~\2\2\u0117\n\3\2\2\2\u0118\u0119\7")
        buf.write("`\2\2\u0119\f\3\2\2\2\u011a\u011b\7/\2\2\u011b\16\3\2")
        buf.write("\2\2\u011c\u011d\7-\2\2\u011d\20\3\2\2\2\u011e\u011f\7")
        buf.write("\61\2\2\u011f\u0120\7\61\2\2\u0120\22\3\2\2\2\u0121\u0122")
        buf.write("\7\61\2\2\u0122\24\3\2\2\2\u0123\u0124\7\'\2\2\u0124\26")
        buf.write("\3\2\2\2\u0125\u0126\7o\2\2\u0126\u0127\7q\2\2\u0127\u0128")
        buf.write("\7f\2\2\u0128\30\3\2\2\2\u0129\u012a\7,\2\2\u012a\u012b")
        buf.write("\7,\2\2\u012b\32\3\2\2\2\u012c\u012d\7>\2\2\u012d\u012e")
        buf.write("\7>\2\2\u012e\34\3\2\2\2\u012f\u0130\7@\2\2\u0130\u0131")
        buf.write("\7@\2\2\u0131\36\3\2\2\2\u0132\u0133\7?\2\2\u0133\u0134")
        buf.write("\7?\2\2\u0134 \3\2\2\2\u0135\u0136\7#\2\2\u0136\u0137")
        buf.write("\7?\2\2\u0137\"\3\2\2\2\u0138\u0139\7>\2\2\u0139$\3\2")
        buf.write("\2\2\u013a\u013b\7>\2\2\u013b\u013c\7?\2\2\u013c&\3\2")
        buf.write("\2\2\u013d\u013e\7@\2\2\u013e(\3\2\2\2\u013f\u0140\7@")
        buf.write("\2\2\u0140\u0141\7?\2\2\u0141*\3\2\2\2\u0142\u0143\7?")
        buf.write("\2\2\u0143\u0144\7@\2\2\u0144,\3\2\2\2\u0145\u0146\7\u0080")
        buf.write("\2\2\u0146.\3\2\2\2\u0147\u0148\7A\2\2\u0148\60\3\2\2")
        buf.write("\2\u0149\u014a\7#\2\2\u014a\62\3\2\2\2\u014b\u014c\7c")
        buf.write("\2\2\u014c\u014d\7d\2\2\u014d\u014e\7u\2\2\u014e\64\3")
        buf.write("\2\2\2\u014f\u0150\7c\2\2\u0150\u0151\7n\2\2\u0151\u0152")
        buf.write("\7n\2\2\u0152\66\3\2\2\2\u0153\u0154\7c\2\2\u0154\u0155")
        buf.write("\7p\2\2\u0155\u0156\7{\2\2\u01568\3\2\2\2\u0157\u0158")
        buf.write("\7d\2\2\u0158\u0159\7k\2\2\u0159\u015a\7p\2\2\u015a:\3")
        buf.write("\2\2\2\u015b\u015c\7e\2\2\u015c\u015d\7j\2\2\u015d\u015e")
        buf.write("\7q\2\2\u015e\u015f\7q\2\2\u015f\u0160\7u\2\2\u0160\u0161")
        buf.write("\7g\2\2\u0161<\3\2\2\2\u0162\u0163\7e\2\2\u0163\u0164")
        buf.write("\7q\2\2\u0164\u0165\7p\2\2\u0165\u0166\7v\2\2\u0166\u0167")
        buf.write("\7g\2\2\u0167\u0168\7z\2\2\u0168\u0169\7v\2\2\u0169\u016a")
        buf.write("\7u\2\2\u016a>\3\2\2\2\u016b\u016c\7i\2\2\u016c\u016d")
        buf.write("\7g\2\2\u016d\u016e\7v\2\2\u016e\u016f\7a\2\2\u016f\u0170")
        buf.write("\7e\2\2\u0170\u0171\7q\2\2\u0171\u0172\7p\2\2\u0172\u0173")
        buf.write("\7v\2\2\u0173\u0174\7g\2\2\u0174\u0175\7z\2\2\u0175\u0176")
        buf.write("\7v\2\2\u0176@\3\2\2\2\u0177\u0178\7i\2\2\u0178\u0179")
        buf.write("\7g\2\2\u0179\u017a\7v\2\2\u017a\u017b\7a\2\2\u017b\u017c")
        buf.write("\7k\2\2\u017c\u017d\7f\2\2\u017d\u017e\7g\2\2\u017e\u017f")
        buf.write("\7p\2\2\u017f\u0180\7v\2\2\u0180B\3\2\2\2\u0181\u0182")
        buf.write("\7j\2\2\u0182\u0183\7c\2\2\u0183\u0184\7u\2\2\u0184\u0185")
        buf.write("\7j\2\2\u0185D\3\2\2\2\u0186\u0187\7j\2\2\u0187\u0188")
        buf.write("\7g\2\2\u0188\u0189\7z\2\2\u0189F\3\2\2\2\u018a\u018b")
        buf.write("\7m\2\2\u018b\u018c\7g\2\2\u018c\u018d\7{\2\2\u018d\u018e")
        buf.write("\7u\2\2\u018eH\3\2\2\2\u018f\u0190\7n\2\2\u0190\u0191")
        buf.write("\7g\2\2\u0191\u0192\7p\2\2\u0192J\3\2\2\2\u0193\u0194")
        buf.write("\7n\2\2\u0194\u0195\7k\2\2\u0195\u0196\7u\2\2\u0196\u0197")
        buf.write("\7v\2\2\u0197L\3\2\2\2\u0198\u0199\7o\2\2\u0199\u019a")
        buf.write("\7c\2\2\u019a\u019b\7z\2\2\u019bN\3\2\2\2\u019c\u019d")
        buf.write("\7o\2\2\u019d\u019e\7k\2\2\u019e\u019f\7p\2\2\u019fP\3")
        buf.write("\2\2\2\u01a0\u01a1\7t\2\2\u01a1\u01a2\7g\2\2\u01a2\u01a3")
        buf.write("\7x\2\2\u01a3\u01a4\7g\2\2\u01a4\u01a5\7t\2\2\u01a5\u01a6")
        buf.write("\7u\2\2\u01a6\u01a7\7g\2\2\u01a7\u01a8\7f\2\2\u01a8R\3")
        buf.write("\2\2\2\u01a9\u01aa\7u\2\2\u01aa\u01ab\7g\2\2\u01ab\u01ac")
        buf.write("\7v\2\2\u01acT\3\2\2\2\u01ad\u01ae\7u\2\2\u01ae\u01af")
        buf.write("\7q\2\2\u01af\u01b0\7t\2\2\u01b0\u01b1\7v\2\2\u01b1\u01b2")
        buf.write("\7g\2\2\u01b2\u01b3\7f\2\2\u01b3V\3\2\2\2\u01b4\u01b5")
        buf.write("\7u\2\2\u01b5\u01b6\7v\2\2\u01b6\u01b7\7t\2\2\u01b7X\3")
        buf.write("\2\2\2\u01b8\u01b9\7u\2\2\u01b9\u01ba\7w\2\2\u01ba\u01bb")
        buf.write("\7o\2\2\u01bbZ\3\2\2\2\u01bc\u01bd\7v\2\2\u01bd\u01be")
        buf.write("\7{\2\2\u01be\u01bf\7r\2\2\u01bf\u01c0\7g\2\2\u01c0\\")
        buf.write("\3\2\2\2\u01c1\u01c2\7g\2\2\u01c2\u01c3\7p\2\2\u01c3\u01c4")
        buf.write("\7f\2\2\u01c4^\3\2\2\2\u01c5\u01c6\7c\2\2\u01c6\u01c7")
        buf.write("\7p\2\2\u01c7\u01c8\7f\2\2\u01c8\u01c9\7?\2\2\u01c9`\3")
        buf.write("\2\2\2\u01ca\u01cb\7q\2\2\u01cb\u01cc\7t\2\2\u01cc\u01cd")
        buf.write("\7?\2\2\u01cdb\3\2\2\2\u01ce\u01cf\7?\2\2\u01cf\u01d0")
        buf.write("\7@\2\2\u01d0\u01d1\7?\2\2\u01d1d\3\2\2\2\u01d2\u01d3")
        buf.write("\7(\2\2\u01d3\u01d4\7?\2\2\u01d4f\3\2\2\2\u01d5\u01d6")
        buf.write("\7~\2\2\u01d6\u01d7\7?\2\2\u01d7h\3\2\2\2\u01d8\u01d9")
        buf.write("\7`\2\2\u01d9\u01da\7?\2\2\u01daj\3\2\2\2\u01db\u01dc")
        buf.write("\7/\2\2\u01dc\u01dd\7?\2\2\u01ddl\3\2\2\2\u01de\u01df")
        buf.write("\7-\2\2\u01df\u01e0\7?\2\2\u01e0n\3\2\2\2\u01e1\u01e2")
        buf.write("\7,\2\2\u01e2\u01e3\7?\2\2\u01e3p\3\2\2\2\u01e4\u01e5")
        buf.write("\7\61\2\2\u01e5\u01e6\7?\2\2\u01e6r\3\2\2\2\u01e7\u01e8")
        buf.write("\7\61\2\2\u01e8\u01e9\7\61\2\2\u01e9\u01ea\7?\2\2\u01ea")
        buf.write("t\3\2\2\2\u01eb\u01ec\7\'\2\2\u01ec\u01ed\7?\2\2\u01ed")
        buf.write("v\3\2\2\2\u01ee\u01ef\7o\2\2\u01ef\u01f0\7q\2\2\u01f0")
        buf.write("\u01f1\7f\2\2\u01f1\u01f2\7?\2\2\u01f2x\3\2\2\2\u01f3")
        buf.write("\u01f4\7,\2\2\u01f4\u01f5\7,\2\2\u01f5\u01f6\7?\2\2\u01f6")
        buf.write("z\3\2\2\2\u01f7\u01f8\7@\2\2\u01f8\u01f9\7@\2\2\u01f9")
        buf.write("\u01fa\7?\2\2\u01fa|\3\2\2\2\u01fb\u01fc\7>\2\2\u01fc")
        buf.write("\u01fd\7>\2\2\u01fd\u01fe\7?\2\2\u01fe~\3\2\2\2\u01ff")
        buf.write("\u0201\7\17\2\2\u0200\u01ff\3\2\2\2\u0200\u0201\3\2\2")
        buf.write("\2\u0201\u0202\3\2\2\2\u0202\u020f\7\f\2\2\u0203\u0205")
        buf.write("\7\"\2\2\u0204\u0203\3\2\2\2\u0205\u0208\3\2\2\2\u0206")
        buf.write("\u0204\3\2\2\2\u0206\u0207\3\2\2\2\u0207\u0210\3\2\2\2")
        buf.write("\u0208\u0206\3\2\2\2\u0209\u020b\7\13\2\2\u020a\u0209")
        buf.write("\3\2\2\2\u020b\u020e\3\2\2\2\u020c\u020a\3\2\2\2\u020c")
        buf.write("\u020d\3\2\2\2\u020d\u0210\3\2\2\2\u020e\u020c\3\2\2\2")
        buf.write("\u020f\u0206\3\2\2\2\u020f\u020c\3\2\2\2\u0210\u0211\3")
        buf.write("\2\2\2\u0211\u0212\b@\2\2\u0212\u0080\3\2\2\2\u0213\u0215")
        buf.write("\7\"\2\2\u0214\u0213\3\2\2\2\u0215\u0216\3\2\2\2\u0216")
        buf.write("\u0214\3\2\2\2\u0216\u0217\3\2\2\2\u0217\u0221\3\2\2\2")
        buf.write("\u0218\u021a\7\13\2\2\u0219\u0218\3\2\2\2\u021a\u021b")
        buf.write("\3\2\2\2\u021b\u0219\3\2\2\2\u021b\u021c\3\2\2\2\u021c")
        buf.write("\u0221\3\2\2\2\u021d\u021e\7^\2\2\u021e\u0221\5\177@\2")
        buf.write("\u021f\u0221\5\u0083B\2\u0220\u0214\3\2\2\2\u0220\u0219")
        buf.write("\3\2\2\2\u0220\u021d\3\2\2\2\u0220\u021f\3\2\2\2\u0221")
        buf.write("\u0222\3\2\2\2\u0222\u0223\bA\3\2\u0223\u0082\3\2\2\2")
        buf.write("\u0224\u0228\5\u0087D\2\u0225\u0227\13\2\2\2\u0226\u0225")
        buf.write("\3\2\2\2\u0227\u022a\3\2\2\2\u0228\u0229\3\2\2\2\u0228")
        buf.write("\u0226\3\2\2\2\u0229\u022b\3\2\2\2\u022a\u0228\3\2\2\2")
        buf.write("\u022b\u022c\5\u0089E\2\u022c\u0235\3\2\2\2\u022d\u0231")
        buf.write("\5\u0085C\2\u022e\u0230\n\2\2\2\u022f\u022e\3\2\2\2\u0230")
        buf.write("\u0233\3\2\2\2\u0231\u022f\3\2\2\2\u0231\u0232\3\2\2\2")
        buf.write("\u0232\u0235\3\2\2\2\u0233\u0231\3\2\2\2\u0234\u0224\3")
        buf.write("\2\2\2\u0234\u022d\3\2\2\2\u0235\u0084\3\2\2\2\u0236\u0237")
        buf.write("\7%\2\2\u0237\u0086\3\2\2\2\u0238\u0239\7*\2\2\u0239\u023a")
        buf.write("\7,\2\2\u023a\u0088\3\2\2\2\u023b\u023c\7,\2\2\u023c\u023d")
        buf.write("\7+\2\2\u023d\u008a\3\2\2\2\u023e\u023f\7,\2\2\u023f\u008c")
        buf.write("\3\2\2\2\u0240\u0241\7c\2\2\u0241\u0242\7u\2\2\u0242\u008e")
        buf.write("\3\2\2\2\u0243\u0244\7\60\2\2\u0244\u0090\3\2\2\2\u0245")
        buf.write("\u0246\7k\2\2\u0246\u0247\7o\2\2\u0247\u0248\7r\2\2\u0248")
        buf.write("\u0249\7q\2\2\u0249\u024a\7t\2\2\u024a\u024b\7v\2\2\u024b")
        buf.write("\u0092\3\2\2\2\u024c\u024d\7r\2\2\u024d\u024e\7t\2\2\u024e")
        buf.write("\u024f\7k\2\2\u024f\u0250\7p\2\2\u0250\u0251\7v\2\2\u0251")
        buf.write("\u0094\3\2\2\2\u0252\u0253\7h\2\2\u0253\u0254\7t\2\2\u0254")
        buf.write("\u0255\7q\2\2\u0255\u0256\7o\2\2\u0256\u0096\3\2\2\2\u0257")
        buf.write("\u0258\7\60\2\2\u0258\u0259\7\60\2\2\u0259\u0098\3\2\2")
        buf.write("\2\u025a\u025b\7u\2\2\u025b\u025c\7g\2\2\u025c\u025d\7")
        buf.write("v\2\2\u025d\u025e\7k\2\2\u025e\u025f\7p\2\2\u025f\u0260")
        buf.write("\7v\2\2\u0260\u0261\7n\2\2\u0261\u0262\7g\2\2\u0262\u0263")
        buf.write("\7x\2\2\u0263\u0264\7g\2\2\u0264\u0265\7n\2\2\u0265\u009a")
        buf.write("\3\2\2\2\u0266\u0267\7u\2\2\u0267\u0268\7c\2\2\u0268\u0269")
        buf.write("\7x\2\2\u0269\u026a\7g\2\2\u026a\u009c\3\2\2\2\u026b\u026c")
        buf.write("\7u\2\2\u026c\u026d\7v\2\2\u026d\u026e\7q\2\2\u026e\u026f")
        buf.write("\7r\2\2\u026f\u009e\3\2\2\2\u0270\u0271\7n\2\2\u0271\u0272")
        buf.write("\7c\2\2\u0272\u0273\7o\2\2\u0273\u0274\7d\2\2\u0274\u0275")
        buf.write("\7f\2\2\u0275\u0276\7c\2\2\u0276\u00a0\3\2\2\2\u0277\u0278")
        buf.write("\7p\2\2\u0278\u0279\7q\2\2\u0279\u027a\7v\2\2\u027a\u00a2")
        buf.write("\3\2\2\2\u027b\u027c\7.\2\2\u027c\u00a4\3\2\2\2\u027d")
        buf.write("\u027e\7e\2\2\u027e\u027f\7q\2\2\u027f\u0280\7p\2\2\u0280")
        buf.write("\u0281\7u\2\2\u0281\u0282\7v\2\2\u0282\u00a6\3\2\2\2\u0283")
        buf.write("\u0284\7c\2\2\u0284\u0285\7y\2\2\u0285\u0286\7c\2\2\u0286")
        buf.write("\u0287\7k\2\2\u0287\u0288\7v\2\2\u0288\u00a8\3\2\2\2\u0289")
        buf.write("\u028a\7c\2\2\u028a\u028b\7u\2\2\u028b\u028c\7u\2\2\u028c")
        buf.write("\u028d\7g\2\2\u028d\u028e\7t\2\2\u028e\u028f\7v\2\2\u028f")
        buf.write("\u00aa\3\2\2\2\u0290\u0291\7x\2\2\u0291\u0292\7c\2\2\u0292")
        buf.write("\u0293\7t\2\2\u0293\u00ac\3\2\2\2\u0294\u0295\7v\2\2\u0295")
        buf.write("\u0296\7t\2\2\u0296\u0297\7c\2\2\u0297\u0298\7r\2\2\u0298")
        buf.write("\u00ae\3\2\2\2\u0299\u029a\7r\2\2\u029a\u029b\7c\2\2\u029b")
        buf.write("\u029c\7u\2\2\u029c\u029d\7u\2\2\u029d\u00b0\3\2\2\2\u029e")
        buf.write("\u029f\7f\2\2\u029f\u02a0\7g\2\2\u02a0\u02a1\7n\2\2\u02a1")
        buf.write("\u00b2\3\2\2\2\u02a2\u02a3\7u\2\2\u02a3\u02a4\7r\2\2\u02a4")
        buf.write("\u02a5\7c\2\2\u02a5\u02a6\7y\2\2\u02a6\u02a7\7p\2\2\u02a7")
        buf.write("\u00b4\3\2\2\2\u02a8\u02a9\7h\2\2\u02a9\u02aa\7k\2\2\u02aa")
        buf.write("\u02ab\7p\2\2\u02ab\u02ac\7c\2\2\u02ac\u02ad\7n\2\2\u02ad")
        buf.write("\u02ae\7n\2\2\u02ae\u02af\7{\2\2\u02af\u00b6\3\2\2\2\u02b0")
        buf.write("\u02b1\7k\2\2\u02b1\u02b2\7p\2\2\u02b2\u02b3\7x\2\2\u02b3")
        buf.write("\u02b4\7c\2\2\u02b4\u02b5\7t\2\2\u02b5\u02b6\7k\2\2\u02b6")
        buf.write("\u02b7\7c\2\2\u02b7\u02b8\7p\2\2\u02b8\u02b9\7v\2\2\u02b9")
        buf.write("\u00b8\3\2\2\2\u02ba\u02bb\7i\2\2\u02bb\u02bc\7q\2\2\u02bc")
        buf.write("\u00ba\3\2\2\2\u02bd\u02be\7d\2\2\u02be\u02bf\7w\2\2\u02bf")
        buf.write("\u02c0\7k\2\2\u02c0\u02c1\7n\2\2\u02c1\u02c2\7v\2\2\u02c2")
        buf.write("\u02c3\7k\2\2\u02c3\u02c4\7p\2\2\u02c4\u00bc\3\2\2\2\u02c5")
        buf.write("\u02c6\7u\2\2\u02c6\u02c7\7g\2\2\u02c7\u02c8\7s\2\2\u02c8")
        buf.write("\u02c9\7w\2\2\u02c9\u02ca\7g\2\2\u02ca\u02cb\7p\2\2\u02cb")
        buf.write("\u02cc\7v\2\2\u02cc\u02cd\7k\2\2\u02cd\u02ce\7c\2\2\u02ce")
        buf.write("\u02cf\7n\2\2\u02cf\u00be\3\2\2\2\u02d0\u02d1\7y\2\2\u02d1")
        buf.write("\u02d2\7j\2\2\u02d2\u02d3\7g\2\2\u02d3\u02d4\7p\2\2\u02d4")
        buf.write("\u00c0\3\2\2\2\u02d5\u02d6\7n\2\2\u02d6\u02d7\7g\2\2\u02d7")
        buf.write("\u02d8\7v\2\2\u02d8\u00c2\3\2\2\2\u02d9\u02da\7k\2\2\u02da")
        buf.write("\u02db\7h\2\2\u02db\u00c4\3\2\2\2\u02dc\u02dd\7g\2\2\u02dd")
        buf.write("\u02de\7n\2\2\u02de\u02df\7k\2\2\u02df\u02e0\7h\2\2\u02e0")
        buf.write("\u00c6\3\2\2\2\u02e1\u02e2\7g\2\2\u02e2\u02e3\7n\2\2\u02e3")
        buf.write("\u02e4\7u\2\2\u02e4\u02e5\7g\2\2\u02e5\u00c8\3\2\2\2\u02e6")
        buf.write("\u02e7\7B\2\2\u02e7\u00ca\3\2\2\2\u02e8\u02e9\7y\2\2\u02e9")
        buf.write("\u02ea\7j\2\2\u02ea\u02eb\7k\2\2\u02eb\u02ec\7n\2\2\u02ec")
        buf.write("\u02ed\7g\2\2\u02ed\u00cc\3\2\2\2\u02ee\u02ef\7i\2\2\u02ef")
        buf.write("\u02f0\7n\2\2\u02f0\u02f1\7q\2\2\u02f1\u02f2\7d\2\2\u02f2")
        buf.write("\u02f3\7c\2\2\u02f3\u02f4\7n\2\2\u02f4\u00ce\3\2\2\2\u02f5")
        buf.write("\u02f6\7f\2\2\u02f6\u02f7\7g\2\2\u02f7\u02f8\7h\2\2\u02f8")
        buf.write("\u00d0\3\2\2\2\u02f9\u02fa\7t\2\2\u02fa\u02fb\7g\2\2\u02fb")
        buf.write("\u02fc\7v\2\2\u02fc\u02fd\7w\2\2\u02fd\u02fe\7t\2\2\u02fe")
        buf.write("\u02ff\7p\2\2\u02ff\u0300\7u\2\2\u0300\u00d2\3\2\2\2\u0301")
        buf.write("\u0302\7g\2\2\u0302\u0303\7z\2\2\u0303\u0304\7k\2\2\u0304")
        buf.write("\u0305\7u\2\2\u0305\u0306\7v\2\2\u0306\u0307\7u\2\2\u0307")
        buf.write("\u00d4\3\2\2\2\u0308\u0309\7y\2\2\u0309\u030a\7j\2\2\u030a")
        buf.write("\u030b\7g\2\2\u030b\u030c\7t\2\2\u030c\u030d\7g\2\2\u030d")
        buf.write("\u00d6\3\2\2\2\u030e\u030f\7?\2\2\u030f\u00d8\3\2\2\2")
        buf.write("\u0310\u0311\7h\2\2\u0311\u0312\7q\2\2\u0312\u0313\7t")
        buf.write("\2\2\u0313\u0314\3\2\2\2\u0314\u0315\bm\4\2\u0315\u00da")
        buf.write("\3\2\2\2\u0316\u0317\7k\2\2\u0317\u0318\7p\2\2\u0318\u0319")
        buf.write("\3\2\2\2\u0319\u031a\bn\5\2\u031a\u00dc\3\2\2\2\u031b")
        buf.write("\u031c\7<\2\2\u031c\u00de\3\2\2\2\u031d\u031e\7P\2\2\u031e")
        buf.write("\u031f\7q\2\2\u031f\u0320\7p\2\2\u0320\u0321\7g\2\2\u0321")
        buf.write("\u00e0\3\2\2\2\u0322\u0323\7c\2\2\u0323\u0324\7v\2\2\u0324")
        buf.write("\u0325\7q\2\2\u0325\u0326\7o\2\2\u0326\u0327\7k\2\2\u0327")
        buf.write("\u0328\7e\2\2\u0328\u0329\7c\2\2\u0329\u032a\7n\2\2\u032a")
        buf.write("\u032b\7n\2\2\u032b\u032c\7{\2\2\u032c\u00e2\3\2\2\2\u032d")
        buf.write("\u032e\7H\2\2\u032e\u032f\7c\2\2\u032f\u0330\7n\2\2\u0330")
        buf.write("\u0331\7u\2\2\u0331\u0337\7g\2\2\u0332\u0333\7V\2\2\u0333")
        buf.write("\u0334\7t\2\2\u0334\u0335\7w\2\2\u0335\u0337\7g\2\2\u0336")
        buf.write("\u032d\3\2\2\2\u0336\u0332\3\2\2\2\u0337\u00e4\3\2\2\2")
        buf.write("\u0338\u0339\7g\2\2\u0339\u033a\7v\2\2\u033a\u033b\7g")
        buf.write("\2\2\u033b\u033c\7t\2\2\u033c\u033d\7p\2\2\u033d\u033e")
        buf.write("\7c\2\2\u033e\u033f\7n\2\2\u033f\u00e6\3\2\2\2\u0340\u0342")
        buf.write("\t\3\2\2\u0341\u0340\3\2\2\2\u0342\u0343\3\2\2\2\u0343")
        buf.write("\u0341\3\2\2\2\u0343\u0344\3\2\2\2\u0344\u035e\3\2\2\2")
        buf.write("\u0345\u0346\7\62\2\2\u0346\u0347\7z\2\2\u0347\u0349\3")
        buf.write("\2\2\2\u0348\u034a\t\4\2\2\u0349\u0348\3\2\2\2\u034a\u034b")
        buf.write("\3\2\2\2\u034b\u0349\3\2\2\2\u034b\u034c\3\2\2\2\u034c")
        buf.write("\u035e\3\2\2\2\u034d\u034e\7\62\2\2\u034e\u034f\7d\2\2")
        buf.write("\u034f\u0351\3\2\2\2\u0350\u0352\t\5\2\2\u0351\u0350\3")
        buf.write("\2\2\2\u0352\u0353\3\2\2\2\u0353\u0351\3\2\2\2\u0353\u0354")
        buf.write("\3\2\2\2\u0354\u035e\3\2\2\2\u0355\u0356\7\62\2\2\u0356")
        buf.write("\u0357\7q\2\2\u0357\u0359\3\2\2\2\u0358\u035a\t\6\2\2")
        buf.write("\u0359\u0358\3\2\2\2\u035a\u035b\3\2\2\2\u035b\u0359\3")
        buf.write("\2\2\2\u035b\u035c\3\2\2\2\u035c\u035e\3\2\2\2\u035d\u0341")
        buf.write("\3\2\2\2\u035d\u0345\3\2\2\2\u035d\u034d\3\2\2\2\u035d")
        buf.write("\u0355\3\2\2\2\u035e\u00e8\3\2\2\2\u035f\u0363\t\7\2\2")
        buf.write("\u0360\u0362\t\b\2\2\u0361\u0360\3\2\2\2\u0362\u0365\3")
        buf.write("\2\2\2\u0363\u0361\3\2\2\2\u0363\u0364\3\2\2\2\u0364\u00ea")
        buf.write("\3\2\2\2\u0365\u0363\3\2\2\2\u0366\u0369\t\t\2\2\u0367")
        buf.write("\u036a\5\u00efx\2\u0368\u036a\5\u00e9u\2\u0369\u0367\3")
        buf.write("\2\2\2\u0369\u0368\3\2\2\2\u036a\u00ec\3\2\2\2\u036b\u036c")
        buf.write("\7/\2\2\u036c\u036d\7@\2\2\u036d\u0371\3\2\2\2\u036e\u0370")
        buf.write("\7\"\2\2\u036f\u036e\3\2\2\2\u0370\u0373\3\2\2\2\u0371")
        buf.write("\u036f\3\2\2\2\u0371\u0372\3\2\2\2\u0372\u0374\3\2\2\2")
        buf.write("\u0373\u0371\3\2\2\2\u0374\u0375\5\u00e9u\2\u0375\u00ee")
        buf.write("\3\2\2\2\u0376\u0377\7\62\2\2\u0377\u0378\7Z\2\2\u0378")
        buf.write("\u037a\3\2\2\2\u0379\u037b\5\u00f1y\2\u037a\u0379\3\2")
        buf.write("\2\2\u037b\u037c\3\2\2\2\u037c\u037a\3\2\2\2\u037c\u037d")
        buf.write("\3\2\2\2\u037d\u00f0\3\2\2\2\u037e\u037f\t\4\2\2\u037f")
        buf.write("\u00f2\3\2\2\2\u0380\u0381\7]\2\2\u0381\u0382\bz\6\2\u0382")
        buf.write("\u00f4\3\2\2\2\u0383\u0384\7_\2\2\u0384\u0385\b{\7\2\u0385")
        buf.write("\u00f6\3\2\2\2\u0386\u0387\7}\2\2\u0387\u0388\b|\b\2\u0388")
        buf.write("\u00f8\3\2\2\2\u0389\u038a\7\177\2\2\u038a\u038b\b}\t")
        buf.write("\2\u038b\u00fa\3\2\2\2\u038c\u038d\7*\2\2\u038d\u038e")
        buf.write("\b~\n\2\u038e\u00fc\3\2\2\2\u038f\u0390\7+\2\2\u0390\u0391")
        buf.write("\b\177\13\2\u0391\u00fe\3\2\2\2\u0392\u0393\7=\2\2\u0393")
        buf.write("\u0100\3\2\2\2\u0394\u0397\5\u0103\u0082\2\u0395\u0397")
        buf.write("\5\u0105\u0083\2\u0396\u0394\3\2\2\2\u0396\u0395\3\2\2")
        buf.write("\2\u0397\u0102\3\2\2\2\u0398\u039d\7)\2\2\u0399\u039c")
        buf.write("\5\u010b\u0086\2\u039a\u039c\n\n\2\2\u039b\u0399\3\2\2")
        buf.write("\2\u039b\u039a\3\2\2\2\u039c\u039f\3\2\2\2\u039d\u039b")
        buf.write("\3\2\2\2\u039d\u039e\3\2\2\2\u039e\u03a0\3\2\2\2\u039f")
        buf.write("\u039d\3\2\2\2\u03a0\u03ab\7)\2\2\u03a1\u03a6\7$\2\2\u03a2")
        buf.write("\u03a5\5\u010b\u0086\2\u03a3\u03a5\n\13\2\2\u03a4\u03a2")
        buf.write("\3\2\2\2\u03a4\u03a3\3\2\2\2\u03a5\u03a8\3\2\2\2\u03a6")
        buf.write("\u03a4\3\2\2\2\u03a6\u03a7\3\2\2\2\u03a7\u03a9\3\2\2\2")
        buf.write("\u03a8\u03a6\3\2\2\2\u03a9\u03ab\7$\2\2\u03aa\u0398\3")
        buf.write("\2\2\2\u03aa\u03a1\3\2\2\2\u03ab\u0104\3\2\2\2\u03ac\u03ad")
        buf.write("\7)\2\2\u03ad\u03ae\7)\2\2\u03ae\u03af\7)\2\2\u03af\u03b3")
        buf.write("\3\2\2\2\u03b0\u03b2\5\u0107\u0084\2\u03b1\u03b0\3\2\2")
        buf.write("\2\u03b2\u03b5\3\2\2\2\u03b3\u03b4\3\2\2\2\u03b3\u03b1")
        buf.write("\3\2\2\2\u03b4\u03b6\3\2\2\2\u03b5\u03b3\3\2\2\2\u03b6")
        buf.write("\u03b7\7)\2\2\u03b7\u03b8\7)\2\2\u03b8\u03c7\7)\2\2\u03b9")
        buf.write("\u03ba\7$\2\2\u03ba\u03bb\7$\2\2\u03bb\u03bc\7$\2\2\u03bc")
        buf.write("\u03c0\3\2\2\2\u03bd\u03bf\5\u0107\u0084\2\u03be\u03bd")
        buf.write("\3\2\2\2\u03bf\u03c2\3\2\2\2\u03c0\u03c1\3\2\2\2\u03c0")
        buf.write("\u03be\3\2\2\2\u03c1\u03c3\3\2\2\2\u03c2\u03c0\3\2\2\2")
        buf.write("\u03c3\u03c4\7$\2\2\u03c4\u03c5\7$\2\2\u03c5\u03c7\7$")
        buf.write("\2\2\u03c6\u03ac\3\2\2\2\u03c6\u03b9\3\2\2\2\u03c7\u0106")
        buf.write("\3\2\2\2\u03c8\u03cb\5\u0109\u0085\2\u03c9\u03cb\5\u010b")
        buf.write("\u0086\2\u03ca\u03c8\3\2\2\2\u03ca\u03c9\3\2\2\2\u03cb")
        buf.write("\u0108\3\2\2\2\u03cc\u03cd\n\f\2\2\u03cd\u010a\3\2\2\2")
        buf.write("\u03ce\u03cf\7^\2\2\u03cf\u03d3\13\2\2\2\u03d0\u03d1\7")
        buf.write("^\2\2\u03d1\u03d3\5\177@\2\u03d2\u03ce\3\2\2\2\u03d2\u03d0")
        buf.write("\3\2\2\2\u03d3\u010c\3\2\2\2\"\2\u0200\u0206\u020c\u020f")
        buf.write("\u0216\u021b\u0220\u0228\u0231\u0234\u0336\u0343\u034b")
        buf.write("\u0353\u035b\u035d\u0363\u0369\u0371\u037c\u0396\u039b")
        buf.write("\u039d\u03a4\u03a6\u03aa\u03b3\u03c0\u03c6\u03ca\u03d2")
        buf.write("\f\3@\2\b\2\2\3m\3\3n\4\3z\5\3{\6\3|\7\3}\b\3~\t\3\177")
        buf.write("\n")
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
    NL = 63
    WS = 64
    COMMENT_START = 65
    OPEN_MULTI_COMMENT = 66
    CLOSE_MULTI_COMMENT = 67
    STAR = 68
    AS = 69
    DOT = 70
    IMPORT = 71
    PRINT = 72
    FROM = 73
    RANGE = 74
    SETINTLEVEL = 75
    SAVE = 76
    STOP = 77
    LAMBDA = 78
    NOT = 79
    COMMA = 80
    CONST = 81
    AWAIT = 82
    ASSERT = 83
    VAR = 84
    TRAP = 85
    PASS = 86
    DEL = 87
    SPAWN = 88
    FINALLY = 89
    INVARIANT = 90
    GO = 91
    BUILTIN = 92
    SEQUENTIAL = 93
    WHEN = 94
    LET = 95
    IF = 96
    ELIF = 97
    ELSE = 98
    AT = 99
    WHILE = 100
    GLOBAL = 101
    DEF = 102
    RETURNS = 103
    EXISTS = 104
    WHERE = 105
    EQ = 106
    FOR = 107
    IN = 108
    COLON = 109
    NONE = 110
    ATOMICALLY = 111
    BOOL = 112
    ETERNAL = 113
    INT = 114
    NAME = 115
    ATOM = 116
    ARROWID = 117
    HEX_INTEGER = 118
    OPEN_BRACK = 119
    CLOSE_BRACK = 120
    OPEN_BRACES = 121
    CLOSE_BRACES = 122
    OPEN_PAREN = 123
    CLOSE_PAREN = 124
    SEMI_COLON = 125
    STRING = 126

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'or'", "'&'", "'|'", "'^'", "'-'", "'+'", "'//'", 
            "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", "'!='", 
            "'<'", "'<='", "'>'", "'>='", "'=>'", "'~'", "'?'", "'!'", "'abs'", 
            "'all'", "'any'", "'bin'", "'choose'", "'contexts'", "'get_context'", 
            "'get_ident'", "'hash'", "'hex'", "'keys'", "'len'", "'list'", 
            "'max'", "'min'", "'reversed'", "'set'", "'sorted'", "'str'", 
            "'sum'", "'type'", "'end'", "'and='", "'or='", "'=>='", "'&='", 
            "'|='", "'^='", "'-='", "'+='", "'*='", "'/='", "'//='", "'%='", 
            "'mod='", "'**='", "'>>='", "'<<='", "'#'", "'(*'", "'*)'", 
            "'*'", "'as'", "'.'", "'import'", "'print'", "'from'", "'..'", 
            "'setintlevel'", "'save'", "'stop'", "'lambda'", "'not'", "','", 
            "'const'", "'await'", "'assert'", "'var'", "'trap'", "'pass'", 
            "'del'", "'spawn'", "'finally'", "'invariant'", "'go'", "'builtin'", 
            "'sequential'", "'when'", "'let'", "'if'", "'elif'", "'else'", 
            "'@'", "'while'", "'global'", "'def'", "'returns'", "'exists'", 
            "'where'", "'='", "'for'", "'in'", "':'", "'None'", "'atomically'", 
            "'eternal'", "'['", "']'", "'{'", "'}'", "'('", "')'", "';'" ]

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
                  "NL", "WS", "COMMENT", "COMMENT_START", "OPEN_MULTI_COMMENT", 
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
            actions[62] = self.NL_action 
            actions[107] = self.FOR_action 
            actions[108] = self.IN_action 
            actions[120] = self.OPEN_BRACK_action 
            actions[121] = self.CLOSE_BRACK_action 
            actions[122] = self.OPEN_BRACES_action 
            actions[123] = self.CLOSE_BRACES_action 
            actions[124] = self.OPEN_PAREN_action 
            actions[125] = self.CLOSE_PAREN_action 
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
     


