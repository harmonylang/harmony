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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2z")
        buf.write("\u03ac\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("\t\u0080\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3")
        buf.write("\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\13\3\13\3")
        buf.write("\f\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3")
        buf.write("\17\3\20\3\20\3\20\3\21\3\21\3\21\3\22\3\22\3\23\3\23")
        buf.write("\3\23\3\24\3\24\3\25\3\25\3\25\3\26\3\26\3\27\3\27\3\30")
        buf.write("\3\30\3\31\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33")
        buf.write("\3\33\3\33\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3 \3 \3")
        buf.write(" \3 \3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3#\3#\3#\3#\3$\3$")
        buf.write("\3$\3$\3%\3%\3%\3%\3%\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3")
        buf.write("\'\3\'\3\'\3(\3(\3(\3(\3)\3)\3)\3)\3)\3*\3*\3*\3*\3+\3")
        buf.write("+\3+\3+\3,\3,\3,\3-\3-\3-\3.\3.\3.\3/\3/\3/\3\60\3\60")
        buf.write("\3\60\3\61\3\61\3\61\3\62\3\62\3\62\3\63\3\63\3\63\3\63")
        buf.write("\3\64\3\64\3\64\3\65\3\65\3\65\3\65\3\65\3\66\3\66\3\66")
        buf.write("\3\66\3\67\3\67\3\67\3\67\38\38\38\38\39\59\u01d6\n9\3")
        buf.write("9\39\79\u01da\n9\f9\169\u01dd\139\39\79\u01e0\n9\f9\16")
        buf.write("9\u01e3\139\59\u01e5\n9\39\39\3:\6:\u01ea\n:\r:\16:\u01eb")
        buf.write("\3:\6:\u01ef\n:\r:\16:\u01f0\3:\3:\3:\5:\u01f6\n:\3:\3")
        buf.write(":\3;\3;\7;\u01fc\n;\f;\16;\u01ff\13;\3;\3;\3;\3;\7;\u0205")
        buf.write("\n;\f;\16;\u0208\13;\5;\u020a\n;\3<\3<\3=\3=\3=\3>\3>")
        buf.write("\3>\3?\3?\3@\3@\3@\3A\3A\3B\3B\3B\3B\3B\3B\3B\3C\3C\3")
        buf.write("C\3C\3C\3C\3D\3D\3D\3D\3D\3E\3E\3E\3F\3F\3F\3F\3F\3F\3")
        buf.write("F\3F\3F\3F\3F\3F\3G\3G\3G\3G\3G\3H\3H\3H\3H\3H\3I\3I\3")
        buf.write("I\3I\3I\3I\3I\3J\3J\3J\3J\3K\3K\3L\3L\3L\3L\3L\3L\3M\3")
        buf.write("M\3M\3M\3M\3M\3N\3N\3N\3N\3N\3N\3N\3O\3O\3O\3O\3P\3P\3")
        buf.write("P\3P\3P\3Q\3Q\3Q\3Q\3Q\3R\3R\3R\3R\3S\3S\3S\3S\3S\3S\3")
        buf.write("T\3T\3T\3T\3T\3T\3T\3T\3U\3U\3U\3U\3U\3U\3U\3U\3U\3U\3")
        buf.write("V\3V\3V\3W\3W\3W\3W\3W\3W\3W\3W\3X\3X\3X\3X\3X\3X\3X\3")
        buf.write("X\3X\3X\3X\3Y\3Y\3Y\3Y\3Y\3Z\3Z\3Z\3Z\3[\3[\3[\3\\\3\\")
        buf.write("\3\\\3\\\3\\\3]\3]\3]\3]\3]\3^\3^\3_\3_\3_\3_\3_\3_\3")
        buf.write("`\3`\3`\3`\3`\3`\3`\3a\3a\3a\3a\3b\3b\3b\3b\3b\3b\3b\3")
        buf.write("b\3c\3c\3c\3c\3c\3c\3c\3d\3d\3d\3d\3d\3d\3e\3e\3f\3f\3")
        buf.write("f\3f\3f\3f\3g\3g\3g\3h\3h\3h\3h\3h\3i\3i\3j\3j\3j\3j\3")
        buf.write("j\3k\3k\3k\3k\3k\3k\3k\3k\3k\3k\3k\3l\3l\3l\3l\3l\3l\3")
        buf.write("l\3l\3l\5l\u030f\nl\3m\3m\3m\3m\3m\3m\3m\3m\3n\6n\u031a")
        buf.write("\nn\rn\16n\u031b\3n\3n\3n\3n\6n\u0322\nn\rn\16n\u0323")
        buf.write("\3n\3n\3n\3n\6n\u032a\nn\rn\16n\u032b\3n\3n\3n\3n\6n\u0332")
        buf.write("\nn\rn\16n\u0333\5n\u0336\nn\3o\3o\7o\u033a\no\fo\16o")
        buf.write("\u033d\13o\3p\3p\3p\5p\u0342\np\3q\3q\3q\3q\7q\u0348\n")
        buf.write("q\fq\16q\u034b\13q\3q\3q\3r\3r\3r\3r\6r\u0353\nr\rr\16")
        buf.write("r\u0354\3s\3s\3t\3t\3t\3u\3u\3u\3v\3v\3v\3w\3w\3w\3x\3")
        buf.write("x\3x\3y\3y\3y\3z\3z\3{\3{\5{\u036f\n{\3|\3|\3|\7|\u0374")
        buf.write("\n|\f|\16|\u0377\13|\3|\3|\3|\3|\7|\u037d\n|\f|\16|\u0380")
        buf.write("\13|\3|\5|\u0383\n|\3}\3}\3}\3}\3}\7}\u038a\n}\f}\16}")
        buf.write("\u038d\13}\3}\3}\3}\3}\3}\3}\3}\3}\7}\u0397\n}\f}\16}")
        buf.write("\u039a\13}\3}\3}\3}\5}\u039f\n}\3~\3~\5~\u03a3\n~\3\177")
        buf.write("\3\177\3\u0080\3\u0080\3\u0080\3\u0080\5\u0080\u03ab\n")
        buf.write("\u0080\5\u01fd\u038b\u0398\2\u0081\3\3\5\4\7\5\t\6\13")
        buf.write("\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37")
        buf.write("\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34")
        buf.write("\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_")
        buf.write("\61a\62c\63e\64g\65i\66k\67m8o9q:s;u\2w<y={>}?\177@\u0081")
        buf.write("A\u0083B\u0085C\u0087D\u0089E\u008bF\u008dG\u008fH\u0091")
        buf.write("I\u0093J\u0095K\u0097L\u0099M\u009bN\u009dO\u009fP\u00a1")
        buf.write("Q\u00a3R\u00a5S\u00a7T\u00a9U\u00abV\u00adW\u00afX\u00b1")
        buf.write("Y\u00b3Z\u00b5[\u00b7\\\u00b9]\u00bb^\u00bd_\u00bf`\u00c1")
        buf.write("a\u00c3b\u00c5c\u00c7d\u00c9e\u00cbf\u00cdg\u00cfh\u00d1")
        buf.write("i\u00d3j\u00d5k\u00d7l\u00d9m\u00dbn\u00ddo\u00dfp\u00e1")
        buf.write("q\u00e3r\u00e5\2\u00e7s\u00e9t\u00ebu\u00edv\u00efw\u00f1")
        buf.write("x\u00f3y\u00f5z\u00f7\2\u00f9\2\u00fb\2\u00fd\2\u00ff")
        buf.write("\2\3\2\r\4\2\f\f\16\17\3\2\62;\5\2\62;CHch\3\2\62\63\3")
        buf.write("\2\629\5\2C\\aac|\6\2\62;C\\aac|\3\2\60\60\6\2\f\f\16")
        buf.write("\17))^^\6\2\f\f\16\17$$^^\3\2^^\2\u03c7\2\3\3\2\2\2\2")
        buf.write("\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3")
        buf.write("\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2")
        buf.write("\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2")
        buf.write("\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3")
        buf.write("\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61")
        buf.write("\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2")
        buf.write("\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3")
        buf.write("\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M")
        buf.write("\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2")
        buf.write("W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2")
        buf.write("\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2")
        buf.write("\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2s\3\2")
        buf.write("\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177")
        buf.write("\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085\3\2\2")
        buf.write("\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2\u008b\3\2\2\2\2\u008d")
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
        buf.write("\2\2\u00db\3\2\2\2\2\u00dd\3\2\2\2\2\u00df\3\2\2\2\2\u00e1")
        buf.write("\3\2\2\2\2\u00e3\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9\3\2\2")
        buf.write("\2\2\u00eb\3\2\2\2\2\u00ed\3\2\2\2\2\u00ef\3\2\2\2\2\u00f1")
        buf.write("\3\2\2\2\2\u00f3\3\2\2\2\2\u00f5\3\2\2\2\3\u0101\3\2\2")
        buf.write("\2\5\u0105\3\2\2\2\7\u0108\3\2\2\2\t\u010a\3\2\2\2\13")
        buf.write("\u010c\3\2\2\2\r\u010e\3\2\2\2\17\u0110\3\2\2\2\21\u0112")
        buf.write("\3\2\2\2\23\u0115\3\2\2\2\25\u0117\3\2\2\2\27\u0119\3")
        buf.write("\2\2\2\31\u011d\3\2\2\2\33\u0120\3\2\2\2\35\u0123\3\2")
        buf.write("\2\2\37\u0126\3\2\2\2!\u0129\3\2\2\2#\u012c\3\2\2\2%\u012e")
        buf.write("\3\2\2\2\'\u0131\3\2\2\2)\u0133\3\2\2\2+\u0136\3\2\2\2")
        buf.write("-\u0138\3\2\2\2/\u013a\3\2\2\2\61\u013c\3\2\2\2\63\u0140")
        buf.write("\3\2\2\2\65\u0148\3\2\2\2\67\u0153\3\2\2\29\u015f\3\2")
        buf.write("\2\2;\u0168\3\2\2\2=\u016c\3\2\2\2?\u0170\3\2\2\2A\u0174")
        buf.write("\3\2\2\2C\u0179\3\2\2\2E\u017d\3\2\2\2G\u0181\3\2\2\2")
        buf.write("I\u0185\3\2\2\2K\u018a\3\2\2\2M\u018f\3\2\2\2O\u0196\3")
        buf.write("\2\2\2Q\u019a\3\2\2\2S\u019f\3\2\2\2U\u01a3\3\2\2\2W\u01a7")
        buf.write("\3\2\2\2Y\u01aa\3\2\2\2[\u01ad\3\2\2\2]\u01b0\3\2\2\2")
        buf.write("_\u01b3\3\2\2\2a\u01b6\3\2\2\2c\u01b9\3\2\2\2e\u01bc\3")
        buf.write("\2\2\2g\u01c0\3\2\2\2i\u01c3\3\2\2\2k\u01c8\3\2\2\2m\u01cc")
        buf.write("\3\2\2\2o\u01d0\3\2\2\2q\u01d5\3\2\2\2s\u01f5\3\2\2\2")
        buf.write("u\u0209\3\2\2\2w\u020b\3\2\2\2y\u020d\3\2\2\2{\u0210\3")
        buf.write("\2\2\2}\u0213\3\2\2\2\177\u0215\3\2\2\2\u0081\u0218\3")
        buf.write("\2\2\2\u0083\u021a\3\2\2\2\u0085\u0221\3\2\2\2\u0087\u0227")
        buf.write("\3\2\2\2\u0089\u022c\3\2\2\2\u008b\u022f\3\2\2\2\u008d")
        buf.write("\u023b\3\2\2\2\u008f\u0240\3\2\2\2\u0091\u0245\3\2\2\2")
        buf.write("\u0093\u024c\3\2\2\2\u0095\u0250\3\2\2\2\u0097\u0252\3")
        buf.write("\2\2\2\u0099\u0258\3\2\2\2\u009b\u025e\3\2\2\2\u009d\u0265")
        buf.write("\3\2\2\2\u009f\u0269\3\2\2\2\u00a1\u026e\3\2\2\2\u00a3")
        buf.write("\u0273\3\2\2\2\u00a5\u0277\3\2\2\2\u00a7\u027d\3\2\2\2")
        buf.write("\u00a9\u0285\3\2\2\2\u00ab\u028f\3\2\2\2\u00ad\u0292\3")
        buf.write("\2\2\2\u00af\u029a\3\2\2\2\u00b1\u02a5\3\2\2\2\u00b3\u02aa")
        buf.write("\3\2\2\2\u00b5\u02ae\3\2\2\2\u00b7\u02b1\3\2\2\2\u00b9")
        buf.write("\u02b6\3\2\2\2\u00bb\u02bb\3\2\2\2\u00bd\u02bd\3\2\2\2")
        buf.write("\u00bf\u02c3\3\2\2\2\u00c1\u02ca\3\2\2\2\u00c3\u02ce\3")
        buf.write("\2\2\2\u00c5\u02d6\3\2\2\2\u00c7\u02dd\3\2\2\2\u00c9\u02e3")
        buf.write("\3\2\2\2\u00cb\u02e5\3\2\2\2\u00cd\u02eb\3\2\2\2\u00cf")
        buf.write("\u02ee\3\2\2\2\u00d1\u02f3\3\2\2\2\u00d3\u02f5\3\2\2\2")
        buf.write("\u00d5\u02fa\3\2\2\2\u00d7\u030e\3\2\2\2\u00d9\u0310\3")
        buf.write("\2\2\2\u00db\u0335\3\2\2\2\u00dd\u0337\3\2\2\2\u00df\u033e")
        buf.write("\3\2\2\2\u00e1\u0343\3\2\2\2\u00e3\u034e\3\2\2\2\u00e5")
        buf.write("\u0356\3\2\2\2\u00e7\u0358\3\2\2\2\u00e9\u035b\3\2\2\2")
        buf.write("\u00eb\u035e\3\2\2\2\u00ed\u0361\3\2\2\2\u00ef\u0364\3")
        buf.write("\2\2\2\u00f1\u0367\3\2\2\2\u00f3\u036a\3\2\2\2\u00f5\u036e")
        buf.write("\3\2\2\2\u00f7\u0382\3\2\2\2\u00f9\u039e\3\2\2\2\u00fb")
        buf.write("\u03a2\3\2\2\2\u00fd\u03a4\3\2\2\2\u00ff\u03aa\3\2\2\2")
        buf.write("\u0101\u0102\7c\2\2\u0102\u0103\7p\2\2\u0103\u0104\7f")
        buf.write("\2\2\u0104\4\3\2\2\2\u0105\u0106\7q\2\2\u0106\u0107\7")
        buf.write("t\2\2\u0107\6\3\2\2\2\u0108\u0109\7(\2\2\u0109\b\3\2\2")
        buf.write("\2\u010a\u010b\7~\2\2\u010b\n\3\2\2\2\u010c\u010d\7`\2")
        buf.write("\2\u010d\f\3\2\2\2\u010e\u010f\7/\2\2\u010f\16\3\2\2\2")
        buf.write("\u0110\u0111\7-\2\2\u0111\20\3\2\2\2\u0112\u0113\7\61")
        buf.write("\2\2\u0113\u0114\7\61\2\2\u0114\22\3\2\2\2\u0115\u0116")
        buf.write("\7\61\2\2\u0116\24\3\2\2\2\u0117\u0118\7\'\2\2\u0118\26")
        buf.write("\3\2\2\2\u0119\u011a\7o\2\2\u011a\u011b\7q\2\2\u011b\u011c")
        buf.write("\7f\2\2\u011c\30\3\2\2\2\u011d\u011e\7,\2\2\u011e\u011f")
        buf.write("\7,\2\2\u011f\32\3\2\2\2\u0120\u0121\7>\2\2\u0121\u0122")
        buf.write("\7>\2\2\u0122\34\3\2\2\2\u0123\u0124\7@\2\2\u0124\u0125")
        buf.write("\7@\2\2\u0125\36\3\2\2\2\u0126\u0127\7?\2\2\u0127\u0128")
        buf.write("\7?\2\2\u0128 \3\2\2\2\u0129\u012a\7#\2\2\u012a\u012b")
        buf.write("\7?\2\2\u012b\"\3\2\2\2\u012c\u012d\7>\2\2\u012d$\3\2")
        buf.write("\2\2\u012e\u012f\7>\2\2\u012f\u0130\7?\2\2\u0130&\3\2")
        buf.write("\2\2\u0131\u0132\7@\2\2\u0132(\3\2\2\2\u0133\u0134\7@")
        buf.write("\2\2\u0134\u0135\7?\2\2\u0135*\3\2\2\2\u0136\u0137\7\u0080")
        buf.write("\2\2\u0137,\3\2\2\2\u0138\u0139\7A\2\2\u0139.\3\2\2\2")
        buf.write("\u013a\u013b\7#\2\2\u013b\60\3\2\2\2\u013c\u013d\7c\2")
        buf.write("\2\u013d\u013e\7d\2\2\u013e\u013f\7u\2\2\u013f\62\3\2")
        buf.write("\2\2\u0140\u0141\7c\2\2\u0141\u0142\7v\2\2\u0142\u0143")
        buf.write("\7N\2\2\u0143\u0144\7c\2\2\u0144\u0145\7d\2\2\u0145\u0146")
        buf.write("\7g\2\2\u0146\u0147\7n\2\2\u0147\64\3\2\2\2\u0148\u0149")
        buf.write("\7e\2\2\u0149\u014a\7q\2\2\u014a\u014b\7w\2\2\u014b\u014c")
        buf.write("\7p\2\2\u014c\u014d\7v\2\2\u014d\u014e\7N\2\2\u014e\u014f")
        buf.write("\7c\2\2\u014f\u0150\7d\2\2\u0150\u0151\7g\2\2\u0151\u0152")
        buf.write("\7n\2\2\u0152\66\3\2\2\2\u0153\u0154\7i\2\2\u0154\u0155")
        buf.write("\7g\2\2\u0155\u0156\7v\2\2\u0156\u0157\7a\2\2\u0157\u0158")
        buf.write("\7e\2\2\u0158\u0159\7q\2\2\u0159\u015a\7p\2\2\u015a\u015b")
        buf.write("\7v\2\2\u015b\u015c\7g\2\2\u015c\u015d\7z\2\2\u015d\u015e")
        buf.write("\7v\2\2\u015e8\3\2\2\2\u015f\u0160\7e\2\2\u0160\u0161")
        buf.write("\7q\2\2\u0161\u0162\7p\2\2\u0162\u0163\7v\2\2\u0163\u0164")
        buf.write("\7g\2\2\u0164\u0165\7z\2\2\u0165\u0166\7v\2\2\u0166\u0167")
        buf.write("\7u\2\2\u0167:\3\2\2\2\u0168\u0169\7o\2\2\u0169\u016a")
        buf.write("\7k\2\2\u016a\u016b\7p\2\2\u016b<\3\2\2\2\u016c\u016d")
        buf.write("\7o\2\2\u016d\u016e\7c\2\2\u016e\u016f\7z\2\2\u016f>\3")
        buf.write("\2\2\2\u0170\u0171\7n\2\2\u0171\u0172\7g\2\2\u0172\u0173")
        buf.write("\7p\2\2\u0173@\3\2\2\2\u0174\u0175\7v\2\2\u0175\u0176")
        buf.write("\7{\2\2\u0176\u0177\7r\2\2\u0177\u0178\7g\2\2\u0178B\3")
        buf.write("\2\2\2\u0179\u017a\7u\2\2\u017a\u017b\7v\2\2\u017b\u017c")
        buf.write("\7t\2\2\u017cD\3\2\2\2\u017d\u017e\7c\2\2\u017e\u017f")
        buf.write("\7p\2\2\u017f\u0180\7{\2\2\u0180F\3\2\2\2\u0181\u0182")
        buf.write("\7c\2\2\u0182\u0183\7n\2\2\u0183\u0184\7n\2\2\u0184H\3")
        buf.write("\2\2\2\u0185\u0186\7m\2\2\u0186\u0187\7g\2\2\u0187\u0188")
        buf.write("\7{\2\2\u0188\u0189\7u\2\2\u0189J\3\2\2\2\u018a\u018b")
        buf.write("\7j\2\2\u018b\u018c\7c\2\2\u018c\u018d\7u\2\2\u018d\u018e")
        buf.write("\7j\2\2\u018eL\3\2\2\2\u018f\u0190\7e\2\2\u0190\u0191")
        buf.write("\7j\2\2\u0191\u0192\7q\2\2\u0192\u0193\7q\2\2\u0193\u0194")
        buf.write("\7u\2\2\u0194\u0195\7g\2\2\u0195N\3\2\2\2\u0196\u0197")
        buf.write("\7g\2\2\u0197\u0198\7p\2\2\u0198\u0199\7f\2\2\u0199P\3")
        buf.write("\2\2\2\u019a\u019b\7c\2\2\u019b\u019c\7p\2\2\u019c\u019d")
        buf.write("\7f\2\2\u019d\u019e\7?\2\2\u019eR\3\2\2\2\u019f\u01a0")
        buf.write("\7q\2\2\u01a0\u01a1\7t\2\2\u01a1\u01a2\7?\2\2\u01a2T\3")
        buf.write("\2\2\2\u01a3\u01a4\7?\2\2\u01a4\u01a5\7@\2\2\u01a5\u01a6")
        buf.write("\7?\2\2\u01a6V\3\2\2\2\u01a7\u01a8\7(\2\2\u01a8\u01a9")
        buf.write("\7?\2\2\u01a9X\3\2\2\2\u01aa\u01ab\7~\2\2\u01ab\u01ac")
        buf.write("\7?\2\2\u01acZ\3\2\2\2\u01ad\u01ae\7`\2\2\u01ae\u01af")
        buf.write("\7?\2\2\u01af\\\3\2\2\2\u01b0\u01b1\7/\2\2\u01b1\u01b2")
        buf.write("\7?\2\2\u01b2^\3\2\2\2\u01b3\u01b4\7-\2\2\u01b4\u01b5")
        buf.write("\7?\2\2\u01b5`\3\2\2\2\u01b6\u01b7\7,\2\2\u01b7\u01b8")
        buf.write("\7?\2\2\u01b8b\3\2\2\2\u01b9\u01ba\7\61\2\2\u01ba\u01bb")
        buf.write("\7?\2\2\u01bbd\3\2\2\2\u01bc\u01bd\7\61\2\2\u01bd\u01be")
        buf.write("\7\61\2\2\u01be\u01bf\7?\2\2\u01bff\3\2\2\2\u01c0\u01c1")
        buf.write("\7\'\2\2\u01c1\u01c2\7?\2\2\u01c2h\3\2\2\2\u01c3\u01c4")
        buf.write("\7o\2\2\u01c4\u01c5\7q\2\2\u01c5\u01c6\7f\2\2\u01c6\u01c7")
        buf.write("\7?\2\2\u01c7j\3\2\2\2\u01c8\u01c9\7,\2\2\u01c9\u01ca")
        buf.write("\7,\2\2\u01ca\u01cb\7?\2\2\u01cbl\3\2\2\2\u01cc\u01cd")
        buf.write("\7@\2\2\u01cd\u01ce\7@\2\2\u01ce\u01cf\7?\2\2\u01cfn\3")
        buf.write("\2\2\2\u01d0\u01d1\7>\2\2\u01d1\u01d2\7>\2\2\u01d2\u01d3")
        buf.write("\7?\2\2\u01d3p\3\2\2\2\u01d4\u01d6\7\17\2\2\u01d5\u01d4")
        buf.write("\3\2\2\2\u01d5\u01d6\3\2\2\2\u01d6\u01d7\3\2\2\2\u01d7")
        buf.write("\u01e4\7\f\2\2\u01d8\u01da\7\"\2\2\u01d9\u01d8\3\2\2\2")
        buf.write("\u01da\u01dd\3\2\2\2\u01db\u01d9\3\2\2\2\u01db\u01dc\3")
        buf.write("\2\2\2\u01dc\u01e5\3\2\2\2\u01dd\u01db\3\2\2\2\u01de\u01e0")
        buf.write("\7\13\2\2\u01df\u01de\3\2\2\2\u01e0\u01e3\3\2\2\2\u01e1")
        buf.write("\u01df\3\2\2\2\u01e1\u01e2\3\2\2\2\u01e2\u01e5\3\2\2\2")
        buf.write("\u01e3\u01e1\3\2\2\2\u01e4\u01db\3\2\2\2\u01e4\u01e1\3")
        buf.write("\2\2\2\u01e5\u01e6\3\2\2\2\u01e6\u01e7\b9\2\2\u01e7r\3")
        buf.write("\2\2\2\u01e8\u01ea\7\"\2\2\u01e9\u01e8\3\2\2\2\u01ea\u01eb")
        buf.write("\3\2\2\2\u01eb\u01e9\3\2\2\2\u01eb\u01ec\3\2\2\2\u01ec")
        buf.write("\u01f6\3\2\2\2\u01ed\u01ef\7\13\2\2\u01ee\u01ed\3\2\2")
        buf.write("\2\u01ef\u01f0\3\2\2\2\u01f0\u01ee\3\2\2\2\u01f0\u01f1")
        buf.write("\3\2\2\2\u01f1\u01f6\3\2\2\2\u01f2\u01f3\7^\2\2\u01f3")
        buf.write("\u01f6\5q9\2\u01f4\u01f6\5u;\2\u01f5\u01e9\3\2\2\2\u01f5")
        buf.write("\u01ee\3\2\2\2\u01f5\u01f2\3\2\2\2\u01f5\u01f4\3\2\2\2")
        buf.write("\u01f6\u01f7\3\2\2\2\u01f7\u01f8\b:\3\2\u01f8t\3\2\2\2")
        buf.write("\u01f9\u01fd\5y=\2\u01fa\u01fc\13\2\2\2\u01fb\u01fa\3")
        buf.write("\2\2\2\u01fc\u01ff\3\2\2\2\u01fd\u01fe\3\2\2\2\u01fd\u01fb")
        buf.write("\3\2\2\2\u01fe\u0200\3\2\2\2\u01ff\u01fd\3\2\2\2\u0200")
        buf.write("\u0201\5{>\2\u0201\u020a\3\2\2\2\u0202\u0206\5w<\2\u0203")
        buf.write("\u0205\n\2\2\2\u0204\u0203\3\2\2\2\u0205\u0208\3\2\2\2")
        buf.write("\u0206\u0204\3\2\2\2\u0206\u0207\3\2\2\2\u0207\u020a\3")
        buf.write("\2\2\2\u0208\u0206\3\2\2\2\u0209\u01f9\3\2\2\2\u0209\u0202")
        buf.write("\3\2\2\2\u020av\3\2\2\2\u020b\u020c\7%\2\2\u020cx\3\2")
        buf.write("\2\2\u020d\u020e\7*\2\2\u020e\u020f\7,\2\2\u020fz\3\2")
        buf.write("\2\2\u0210\u0211\7,\2\2\u0211\u0212\7+\2\2\u0212|\3\2")
        buf.write("\2\2\u0213\u0214\7,\2\2\u0214~\3\2\2\2\u0215\u0216\7c")
        buf.write("\2\2\u0216\u0217\7u\2\2\u0217\u0080\3\2\2\2\u0218\u0219")
        buf.write("\7\60\2\2\u0219\u0082\3\2\2\2\u021a\u021b\7k\2\2\u021b")
        buf.write("\u021c\7o\2\2\u021c\u021d\7r\2\2\u021d\u021e\7q\2\2\u021e")
        buf.write("\u021f\7t\2\2\u021f\u0220\7v\2\2\u0220\u0084\3\2\2\2\u0221")
        buf.write("\u0222\7r\2\2\u0222\u0223\7t\2\2\u0223\u0224\7k\2\2\u0224")
        buf.write("\u0225\7p\2\2\u0225\u0226\7v\2\2\u0226\u0086\3\2\2\2\u0227")
        buf.write("\u0228\7h\2\2\u0228\u0229\7t\2\2\u0229\u022a\7q\2\2\u022a")
        buf.write("\u022b\7o\2\2\u022b\u0088\3\2\2\2\u022c\u022d\7\60\2\2")
        buf.write("\u022d\u022e\7\60\2\2\u022e\u008a\3\2\2\2\u022f\u0230")
        buf.write("\7u\2\2\u0230\u0231\7g\2\2\u0231\u0232\7v\2\2\u0232\u0233")
        buf.write("\7k\2\2\u0233\u0234\7p\2\2\u0234\u0235\7v\2\2\u0235\u0236")
        buf.write("\7n\2\2\u0236\u0237\7g\2\2\u0237\u0238\7x\2\2\u0238\u0239")
        buf.write("\7g\2\2\u0239\u023a\7n\2\2\u023a\u008c\3\2\2\2\u023b\u023c")
        buf.write("\7u\2\2\u023c\u023d\7c\2\2\u023d\u023e\7x\2\2\u023e\u023f")
        buf.write("\7g\2\2\u023f\u008e\3\2\2\2\u0240\u0241\7u\2\2\u0241\u0242")
        buf.write("\7v\2\2\u0242\u0243\7q\2\2\u0243\u0244\7r\2\2\u0244\u0090")
        buf.write("\3\2\2\2\u0245\u0246\7n\2\2\u0246\u0247\7c\2\2\u0247\u0248")
        buf.write("\7o\2\2\u0248\u0249\7d\2\2\u0249\u024a\7f\2\2\u024a\u024b")
        buf.write("\7c\2\2\u024b\u0092\3\2\2\2\u024c\u024d\7p\2\2\u024d\u024e")
        buf.write("\7q\2\2\u024e\u024f\7v\2\2\u024f\u0094\3\2\2\2\u0250\u0251")
        buf.write("\7.\2\2\u0251\u0096\3\2\2\2\u0252\u0253\7e\2\2\u0253\u0254")
        buf.write("\7q\2\2\u0254\u0255\7p\2\2\u0255\u0256\7u\2\2\u0256\u0257")
        buf.write("\7v\2\2\u0257\u0098\3\2\2\2\u0258\u0259\7c\2\2\u0259\u025a")
        buf.write("\7y\2\2\u025a\u025b\7c\2\2\u025b\u025c\7k\2\2\u025c\u025d")
        buf.write("\7v\2\2\u025d\u009a\3\2\2\2\u025e\u025f\7c\2\2\u025f\u0260")
        buf.write("\7u\2\2\u0260\u0261\7u\2\2\u0261\u0262\7g\2\2\u0262\u0263")
        buf.write("\7t\2\2\u0263\u0264\7v\2\2\u0264\u009c\3\2\2\2\u0265\u0266")
        buf.write("\7x\2\2\u0266\u0267\7c\2\2\u0267\u0268\7t\2\2\u0268\u009e")
        buf.write("\3\2\2\2\u0269\u026a\7v\2\2\u026a\u026b\7t\2\2\u026b\u026c")
        buf.write("\7c\2\2\u026c\u026d\7r\2\2\u026d\u00a0\3\2\2\2\u026e\u026f")
        buf.write("\7r\2\2\u026f\u0270\7c\2\2\u0270\u0271\7u\2\2\u0271\u0272")
        buf.write("\7u\2\2\u0272\u00a2\3\2\2\2\u0273\u0274\7f\2\2\u0274\u0275")
        buf.write("\7g\2\2\u0275\u0276\7n\2\2\u0276\u00a4\3\2\2\2\u0277\u0278")
        buf.write("\7u\2\2\u0278\u0279\7r\2\2\u0279\u027a\7c\2\2\u027a\u027b")
        buf.write("\7y\2\2\u027b\u027c\7p\2\2\u027c\u00a6\3\2\2\2\u027d\u027e")
        buf.write("\7h\2\2\u027e\u027f\7k\2\2\u027f\u0280\7p\2\2\u0280\u0281")
        buf.write("\7c\2\2\u0281\u0282\7n\2\2\u0282\u0283\7n\2\2\u0283\u0284")
        buf.write("\7{\2\2\u0284\u00a8\3\2\2\2\u0285\u0286\7k\2\2\u0286\u0287")
        buf.write("\7p\2\2\u0287\u0288\7x\2\2\u0288\u0289\7c\2\2\u0289\u028a")
        buf.write("\7t\2\2\u028a\u028b\7k\2\2\u028b\u028c\7c\2\2\u028c\u028d")
        buf.write("\7p\2\2\u028d\u028e\7v\2\2\u028e\u00aa\3\2\2\2\u028f\u0290")
        buf.write("\7i\2\2\u0290\u0291\7q\2\2\u0291\u00ac\3\2\2\2\u0292\u0293")
        buf.write("\7d\2\2\u0293\u0294\7w\2\2\u0294\u0295\7k\2\2\u0295\u0296")
        buf.write("\7n\2\2\u0296\u0297\7v\2\2\u0297\u0298\7k\2\2\u0298\u0299")
        buf.write("\7p\2\2\u0299\u00ae\3\2\2\2\u029a\u029b\7u\2\2\u029b\u029c")
        buf.write("\7g\2\2\u029c\u029d\7s\2\2\u029d\u029e\7w\2\2\u029e\u029f")
        buf.write("\7g\2\2\u029f\u02a0\7p\2\2\u02a0\u02a1\7v\2\2\u02a1\u02a2")
        buf.write("\7k\2\2\u02a2\u02a3\7c\2\2\u02a3\u02a4\7n\2\2\u02a4\u00b0")
        buf.write("\3\2\2\2\u02a5\u02a6\7y\2\2\u02a6\u02a7\7j\2\2\u02a7\u02a8")
        buf.write("\7g\2\2\u02a8\u02a9\7p\2\2\u02a9\u00b2\3\2\2\2\u02aa\u02ab")
        buf.write("\7n\2\2\u02ab\u02ac\7g\2\2\u02ac\u02ad\7v\2\2\u02ad\u00b4")
        buf.write("\3\2\2\2\u02ae\u02af\7k\2\2\u02af\u02b0\7h\2\2\u02b0\u00b6")
        buf.write("\3\2\2\2\u02b1\u02b2\7g\2\2\u02b2\u02b3\7n\2\2\u02b3\u02b4")
        buf.write("\7k\2\2\u02b4\u02b5\7h\2\2\u02b5\u00b8\3\2\2\2\u02b6\u02b7")
        buf.write("\7g\2\2\u02b7\u02b8\7n\2\2\u02b8\u02b9\7u\2\2\u02b9\u02ba")
        buf.write("\7g\2\2\u02ba\u00ba\3\2\2\2\u02bb\u02bc\7B\2\2\u02bc\u00bc")
        buf.write("\3\2\2\2\u02bd\u02be\7y\2\2\u02be\u02bf\7j\2\2\u02bf\u02c0")
        buf.write("\7k\2\2\u02c0\u02c1\7n\2\2\u02c1\u02c2\7g\2\2\u02c2\u00be")
        buf.write("\3\2\2\2\u02c3\u02c4\7i\2\2\u02c4\u02c5\7n\2\2\u02c5\u02c6")
        buf.write("\7q\2\2\u02c6\u02c7\7d\2\2\u02c7\u02c8\7c\2\2\u02c8\u02c9")
        buf.write("\7n\2\2\u02c9\u00c0\3\2\2\2\u02ca\u02cb\7f\2\2\u02cb\u02cc")
        buf.write("\7g\2\2\u02cc\u02cd\7h\2\2\u02cd\u00c2\3\2\2\2\u02ce\u02cf")
        buf.write("\7t\2\2\u02cf\u02d0\7g\2\2\u02d0\u02d1\7v\2\2\u02d1\u02d2")
        buf.write("\7w\2\2\u02d2\u02d3\7t\2\2\u02d3\u02d4\7p\2\2\u02d4\u02d5")
        buf.write("\7u\2\2\u02d5\u00c4\3\2\2\2\u02d6\u02d7\7g\2\2\u02d7\u02d8")
        buf.write("\7z\2\2\u02d8\u02d9\7k\2\2\u02d9\u02da\7u\2\2\u02da\u02db")
        buf.write("\7v\2\2\u02db\u02dc\7u\2\2\u02dc\u00c6\3\2\2\2\u02dd\u02de")
        buf.write("\7y\2\2\u02de\u02df\7j\2\2\u02df\u02e0\7g\2\2\u02e0\u02e1")
        buf.write("\7t\2\2\u02e1\u02e2\7g\2\2\u02e2\u00c8\3\2\2\2\u02e3\u02e4")
        buf.write("\7?\2\2\u02e4\u00ca\3\2\2\2\u02e5\u02e6\7h\2\2\u02e6\u02e7")
        buf.write("\7q\2\2\u02e7\u02e8\7t\2\2\u02e8\u02e9\3\2\2\2\u02e9\u02ea")
        buf.write("\bf\4\2\u02ea\u00cc\3\2\2\2\u02eb\u02ec\7?\2\2\u02ec\u02ed")
        buf.write("\7@\2\2\u02ed\u00ce\3\2\2\2\u02ee\u02ef\7k\2\2\u02ef\u02f0")
        buf.write("\7p\2\2\u02f0\u02f1\3\2\2\2\u02f1\u02f2\bh\5\2\u02f2\u00d0")
        buf.write("\3\2\2\2\u02f3\u02f4\7<\2\2\u02f4\u00d2\3\2\2\2\u02f5")
        buf.write("\u02f6\7P\2\2\u02f6\u02f7\7q\2\2\u02f7\u02f8\7p\2\2\u02f8")
        buf.write("\u02f9\7g\2\2\u02f9\u00d4\3\2\2\2\u02fa\u02fb\7c\2\2\u02fb")
        buf.write("\u02fc\7v\2\2\u02fc\u02fd\7q\2\2\u02fd\u02fe\7o\2\2\u02fe")
        buf.write("\u02ff\7k\2\2\u02ff\u0300\7e\2\2\u0300\u0301\7c\2\2\u0301")
        buf.write("\u0302\7n\2\2\u0302\u0303\7n\2\2\u0303\u0304\7{\2\2\u0304")
        buf.write("\u00d6\3\2\2\2\u0305\u0306\7H\2\2\u0306\u0307\7c\2\2\u0307")
        buf.write("\u0308\7n\2\2\u0308\u0309\7u\2\2\u0309\u030f\7g\2\2\u030a")
        buf.write("\u030b\7V\2\2\u030b\u030c\7t\2\2\u030c\u030d\7w\2\2\u030d")
        buf.write("\u030f\7g\2\2\u030e\u0305\3\2\2\2\u030e\u030a\3\2\2\2")
        buf.write("\u030f\u00d8\3\2\2\2\u0310\u0311\7g\2\2\u0311\u0312\7")
        buf.write("v\2\2\u0312\u0313\7g\2\2\u0313\u0314\7t\2\2\u0314\u0315")
        buf.write("\7p\2\2\u0315\u0316\7c\2\2\u0316\u0317\7n\2\2\u0317\u00da")
        buf.write("\3\2\2\2\u0318\u031a\t\3\2\2\u0319\u0318\3\2\2\2\u031a")
        buf.write("\u031b\3\2\2\2\u031b\u0319\3\2\2\2\u031b\u031c\3\2\2\2")
        buf.write("\u031c\u0336\3\2\2\2\u031d\u031e\7\62\2\2\u031e\u031f")
        buf.write("\7z\2\2\u031f\u0321\3\2\2\2\u0320\u0322\t\4\2\2\u0321")
        buf.write("\u0320\3\2\2\2\u0322\u0323\3\2\2\2\u0323\u0321\3\2\2\2")
        buf.write("\u0323\u0324\3\2\2\2\u0324\u0336\3\2\2\2\u0325\u0326\7")
        buf.write("\62\2\2\u0326\u0327\7d\2\2\u0327\u0329\3\2\2\2\u0328\u032a")
        buf.write("\t\5\2\2\u0329\u0328\3\2\2\2\u032a\u032b\3\2\2\2\u032b")
        buf.write("\u0329\3\2\2\2\u032b\u032c\3\2\2\2\u032c\u0336\3\2\2\2")
        buf.write("\u032d\u032e\7\62\2\2\u032e\u032f\7q\2\2\u032f\u0331\3")
        buf.write("\2\2\2\u0330\u0332\t\6\2\2\u0331\u0330\3\2\2\2\u0332\u0333")
        buf.write("\3\2\2\2\u0333\u0331\3\2\2\2\u0333\u0334\3\2\2\2\u0334")
        buf.write("\u0336\3\2\2\2\u0335\u0319\3\2\2\2\u0335\u031d\3\2\2\2")
        buf.write("\u0335\u0325\3\2\2\2\u0335\u032d\3\2\2\2\u0336\u00dc\3")
        buf.write("\2\2\2\u0337\u033b\t\7\2\2\u0338\u033a\t\b\2\2\u0339\u0338")
        buf.write("\3\2\2\2\u033a\u033d\3\2\2\2\u033b\u0339\3\2\2\2\u033b")
        buf.write("\u033c\3\2\2\2\u033c\u00de\3\2\2\2\u033d\u033b\3\2\2\2")
        buf.write("\u033e\u0341\t\t\2\2\u033f\u0342\5\u00e3r\2\u0340\u0342")
        buf.write("\5\u00ddo\2\u0341\u033f\3\2\2\2\u0341\u0340\3\2\2\2\u0342")
        buf.write("\u00e0\3\2\2\2\u0343\u0344\7/\2\2\u0344\u0345\7@\2\2\u0345")
        buf.write("\u0349\3\2\2\2\u0346\u0348\7\"\2\2\u0347\u0346\3\2\2\2")
        buf.write("\u0348\u034b\3\2\2\2\u0349\u0347\3\2\2\2\u0349\u034a\3")
        buf.write("\2\2\2\u034a\u034c\3\2\2\2\u034b\u0349\3\2\2\2\u034c\u034d")
        buf.write("\5\u00ddo\2\u034d\u00e2\3\2\2\2\u034e\u034f\7\62\2\2\u034f")
        buf.write("\u0350\7Z\2\2\u0350\u0352\3\2\2\2\u0351\u0353\5\u00e5")
        buf.write("s\2\u0352\u0351\3\2\2\2\u0353\u0354\3\2\2\2\u0354\u0352")
        buf.write("\3\2\2\2\u0354\u0355\3\2\2\2\u0355\u00e4\3\2\2\2\u0356")
        buf.write("\u0357\t\4\2\2\u0357\u00e6\3\2\2\2\u0358\u0359\7]\2\2")
        buf.write("\u0359\u035a\bt\6\2\u035a\u00e8\3\2\2\2\u035b\u035c\7")
        buf.write("_\2\2\u035c\u035d\bu\7\2\u035d\u00ea\3\2\2\2\u035e\u035f")
        buf.write("\7}\2\2\u035f\u0360\bv\b\2\u0360\u00ec\3\2\2\2\u0361\u0362")
        buf.write("\7\177\2\2\u0362\u0363\bw\t\2\u0363\u00ee\3\2\2\2\u0364")
        buf.write("\u0365\7*\2\2\u0365\u0366\bx\n\2\u0366\u00f0\3\2\2\2\u0367")
        buf.write("\u0368\7+\2\2\u0368\u0369\by\13\2\u0369\u00f2\3\2\2\2")
        buf.write("\u036a\u036b\7=\2\2\u036b\u00f4\3\2\2\2\u036c\u036f\5")
        buf.write("\u00f7|\2\u036d\u036f\5\u00f9}\2\u036e\u036c\3\2\2\2\u036e")
        buf.write("\u036d\3\2\2\2\u036f\u00f6\3\2\2\2\u0370\u0375\7)\2\2")
        buf.write("\u0371\u0374\5\u00ff\u0080\2\u0372\u0374\n\n\2\2\u0373")
        buf.write("\u0371\3\2\2\2\u0373\u0372\3\2\2\2\u0374\u0377\3\2\2\2")
        buf.write("\u0375\u0373\3\2\2\2\u0375\u0376\3\2\2\2\u0376\u0378\3")
        buf.write("\2\2\2\u0377\u0375\3\2\2\2\u0378\u0383\7)\2\2\u0379\u037e")
        buf.write("\7$\2\2\u037a\u037d\5\u00ff\u0080\2\u037b\u037d\n\13\2")
        buf.write("\2\u037c\u037a\3\2\2\2\u037c\u037b\3\2\2\2\u037d\u0380")
        buf.write("\3\2\2\2\u037e\u037c\3\2\2\2\u037e\u037f\3\2\2\2\u037f")
        buf.write("\u0381\3\2\2\2\u0380\u037e\3\2\2\2\u0381\u0383\7$\2\2")
        buf.write("\u0382\u0370\3\2\2\2\u0382\u0379\3\2\2\2\u0383\u00f8\3")
        buf.write("\2\2\2\u0384\u0385\7)\2\2\u0385\u0386\7)\2\2\u0386\u0387")
        buf.write("\7)\2\2\u0387\u038b\3\2\2\2\u0388\u038a\5\u00fb~\2\u0389")
        buf.write("\u0388\3\2\2\2\u038a\u038d\3\2\2\2\u038b\u038c\3\2\2\2")
        buf.write("\u038b\u0389\3\2\2\2\u038c\u038e\3\2\2\2\u038d\u038b\3")
        buf.write("\2\2\2\u038e\u038f\7)\2\2\u038f\u0390\7)\2\2\u0390\u039f")
        buf.write("\7)\2\2\u0391\u0392\7$\2\2\u0392\u0393\7$\2\2\u0393\u0394")
        buf.write("\7$\2\2\u0394\u0398\3\2\2\2\u0395\u0397\5\u00fb~\2\u0396")
        buf.write("\u0395\3\2\2\2\u0397\u039a\3\2\2\2\u0398\u0399\3\2\2\2")
        buf.write("\u0398\u0396\3\2\2\2\u0399\u039b\3\2\2\2\u039a\u0398\3")
        buf.write("\2\2\2\u039b\u039c\7$\2\2\u039c\u039d\7$\2\2\u039d\u039f")
        buf.write("\7$\2\2\u039e\u0384\3\2\2\2\u039e\u0391\3\2\2\2\u039f")
        buf.write("\u00fa\3\2\2\2\u03a0\u03a3\5\u00fd\177\2\u03a1\u03a3\5")
        buf.write("\u00ff\u0080\2\u03a2\u03a0\3\2\2\2\u03a2\u03a1\3\2\2\2")
        buf.write("\u03a3\u00fc\3\2\2\2\u03a4\u03a5\n\f\2\2\u03a5\u00fe\3")
        buf.write("\2\2\2\u03a6\u03a7\7^\2\2\u03a7\u03ab\13\2\2\2\u03a8\u03a9")
        buf.write("\7^\2\2\u03a9\u03ab\5q9\2\u03aa\u03a6\3\2\2\2\u03aa\u03a8")
        buf.write("\3\2\2\2\u03ab\u0100\3\2\2\2\"\2\u01d5\u01db\u01e1\u01e4")
        buf.write("\u01eb\u01f0\u01f5\u01fd\u0206\u0209\u030e\u031b\u0323")
        buf.write("\u032b\u0333\u0335\u033b\u0341\u0349\u0354\u036e\u0373")
        buf.write("\u0375\u037c\u037e\u0382\u038b\u0398\u039e\u03a2\u03aa")
        buf.write("\f\39\2\b\2\2\3f\3\3h\4\3t\5\3u\6\3v\7\3w\b\3x\t\3y\n")
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
    NL = 56
    WS = 57
    COMMENT_START = 58
    OPEN_MULTI_COMMENT = 59
    CLOSE_MULTI_COMMENT = 60
    STAR = 61
    AS = 62
    DOT = 63
    IMPORT = 64
    PRINT = 65
    FROM = 66
    RANGE = 67
    SETINTLEVEL = 68
    SAVE = 69
    STOP = 70
    LAMBDA = 71
    NOT = 72
    COMMA = 73
    CONST = 74
    AWAIT = 75
    ASSERT = 76
    VAR = 77
    TRAP = 78
    PASS = 79
    DEL = 80
    SPAWN = 81
    FINALLY = 82
    INVARIANT = 83
    GO = 84
    BUILTIN = 85
    SEQUENTIAL = 86
    WHEN = 87
    LET = 88
    IF = 89
    ELIF = 90
    ELSE = 91
    AT = 92
    WHILE = 93
    GLOBAL = 94
    DEF = 95
    RETURNS = 96
    EXISTS = 97
    WHERE = 98
    EQ = 99
    FOR = 100
    IMPLIES = 101
    IN = 102
    COLON = 103
    NONE = 104
    ATOMICALLY = 105
    BOOL = 106
    ETERNAL = 107
    INT = 108
    NAME = 109
    ATOM = 110
    ARROWID = 111
    HEX_INTEGER = 112
    OPEN_BRACK = 113
    CLOSE_BRACK = 114
    OPEN_BRACES = 115
    CLOSE_BRACES = 116
    OPEN_PAREN = 117
    CLOSE_PAREN = 118
    SEMI_COLON = 119
    STRING = 120

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'or'", "'&'", "'|'", "'^'", "'-'", "'+'", "'//'", 
            "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", "'!='", 
            "'<'", "'<='", "'>'", "'>='", "'~'", "'?'", "'!'", "'abs'", 
            "'atLabel'", "'countLabel'", "'get_context'", "'contexts'", 
            "'min'", "'max'", "'len'", "'type'", "'str'", "'any'", "'all'", 
            "'keys'", "'hash'", "'choose'", "'end'", "'and='", "'or='", 
            "'=>='", "'&='", "'|='", "'^='", "'-='", "'+='", "'*='", "'/='", 
            "'//='", "'%='", "'mod='", "'**='", "'>>='", "'<<='", "'#'", 
            "'(*'", "'*)'", "'*'", "'as'", "'.'", "'import'", "'print'", 
            "'from'", "'..'", "'setintlevel'", "'save'", "'stop'", "'lambda'", 
            "'not'", "','", "'const'", "'await'", "'assert'", "'var'", "'trap'", 
            "'pass'", "'del'", "'spawn'", "'finally'", "'invariant'", "'go'", 
            "'builtin'", "'sequential'", "'when'", "'let'", "'if'", "'elif'", 
            "'else'", "'@'", "'while'", "'global'", "'def'", "'returns'", 
            "'exists'", "'where'", "'='", "'for'", "'=>'", "'in'", "':'", 
            "'None'", "'atomically'", "'eternal'", "'['", "']'", "'{'", 
            "'}'", "'('", "')'", "';'" ]

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
                  "T__50", "T__51", "T__52", "T__53", "T__54", "NL", "WS", 
                  "COMMENT", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
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
            actions[55] = self.NL_action 
            actions[100] = self.FOR_action 
            actions[102] = self.IN_action 
            actions[114] = self.OPEN_BRACK_action 
            actions[115] = self.CLOSE_BRACK_action 
            actions[116] = self.OPEN_BRACES_action 
            actions[117] = self.CLOSE_BRACES_action 
            actions[118] = self.OPEN_PAREN_action 
            actions[119] = self.CLOSE_PAREN_action 
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
     


