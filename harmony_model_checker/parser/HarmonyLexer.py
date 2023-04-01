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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2y")
        buf.write("\u03a3\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("y\ty\4z\tz\4{\t{\4|\t|\4}\t}\4~\t~\4\177\t\177\3\2\3\2")
        buf.write("\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3")
        buf.write("\b\3\b\3\t\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\f\3\f\3")
        buf.write("\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3\17\3\20\3\20\3\20")
        buf.write("\3\21\3\21\3\21\3\22\3\22\3\23\3\23\3\23\3\24\3\24\3\25")
        buf.write("\3\25\3\25\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3\31")
        buf.write("\3\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\33\3\33")
        buf.write("\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\34\3\34")
        buf.write("\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\35")
        buf.write("\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\36\3\36\3\36")
        buf.write("\3\36\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3!\3!\3!\3!\3!\3")
        buf.write("\"\3\"\3\"\3\"\3#\3#\3#\3#\3$\3$\3$\3$\3%\3%\3%\3%\3%")
        buf.write("\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3\'\3(\3(\3(\3")
        buf.write("(\3)\3)\3)\3)\3)\3*\3*\3*\3*\3+\3+\3+\3+\3,\3,\3,\3-\3")
        buf.write("-\3-\3.\3.\3.\3/\3/\3/\3\60\3\60\3\60\3\61\3\61\3\61\3")
        buf.write("\62\3\62\3\62\3\63\3\63\3\63\3\63\3\64\3\64\3\64\3\65")
        buf.write("\3\65\3\65\3\65\3\65\3\66\3\66\3\66\3\66\3\67\3\67\3\67")
        buf.write("\3\67\38\38\38\38\39\59\u01d4\n9\39\39\79\u01d8\n9\f9")
        buf.write("\169\u01db\139\39\79\u01de\n9\f9\169\u01e1\139\59\u01e3")
        buf.write("\n9\39\39\3:\6:\u01e8\n:\r:\16:\u01e9\3:\6:\u01ed\n:\r")
        buf.write(":\16:\u01ee\3:\3:\3:\5:\u01f4\n:\3:\3:\3;\3;\7;\u01fa")
        buf.write("\n;\f;\16;\u01fd\13;\3;\3;\3;\3;\7;\u0203\n;\f;\16;\u0206")
        buf.write("\13;\5;\u0208\n;\3<\3<\3=\3=\3=\3>\3>\3>\3?\3?\3@\3@\3")
        buf.write("@\3A\3A\3B\3B\3B\3B\3B\3B\3B\3C\3C\3C\3C\3C\3C\3D\3D\3")
        buf.write("D\3D\3D\3E\3E\3E\3F\3F\3F\3F\3F\3F\3F\3F\3F\3F\3F\3F\3")
        buf.write("G\3G\3G\3G\3G\3H\3H\3H\3H\3H\3I\3I\3I\3I\3I\3I\3I\3J\3")
        buf.write("J\3J\3J\3K\3K\3L\3L\3L\3L\3L\3L\3M\3M\3M\3M\3M\3M\3N\3")
        buf.write("N\3N\3N\3N\3N\3N\3O\3O\3O\3O\3P\3P\3P\3P\3P\3Q\3Q\3Q\3")
        buf.write("Q\3Q\3R\3R\3R\3R\3S\3S\3S\3S\3S\3S\3T\3T\3T\3T\3T\3T\3")
        buf.write("T\3T\3U\3U\3U\3U\3U\3U\3U\3U\3U\3U\3V\3V\3V\3W\3W\3W\3")
        buf.write("W\3W\3W\3W\3W\3X\3X\3X\3X\3X\3X\3X\3X\3X\3X\3X\3Y\3Y\3")
        buf.write("Y\3Y\3Y\3Z\3Z\3Z\3Z\3[\3[\3[\3\\\3\\\3\\\3\\\3\\\3]\3")
        buf.write("]\3]\3]\3]\3^\3^\3_\3_\3_\3_\3_\3_\3`\3`\3`\3`\3a\3a\3")
        buf.write("a\3a\3a\3a\3a\3a\3b\3b\3b\3b\3b\3b\3b\3c\3c\3c\3c\3c\3")
        buf.write("c\3d\3d\3e\3e\3e\3e\3e\3e\3f\3f\3f\3g\3g\3g\3g\3g\3h\3")
        buf.write("h\3i\3i\3i\3i\3i\3j\3j\3j\3j\3j\3j\3j\3j\3j\3j\3j\3k\3")
        buf.write("k\3k\3k\3k\3k\3k\3k\3k\5k\u0306\nk\3l\3l\3l\3l\3l\3l\3")
        buf.write("l\3l\3m\6m\u0311\nm\rm\16m\u0312\3m\3m\3m\3m\6m\u0319")
        buf.write("\nm\rm\16m\u031a\3m\3m\3m\3m\6m\u0321\nm\rm\16m\u0322")
        buf.write("\3m\3m\3m\3m\6m\u0329\nm\rm\16m\u032a\5m\u032d\nm\3n\3")
        buf.write("n\7n\u0331\nn\fn\16n\u0334\13n\3o\3o\3o\5o\u0339\no\3")
        buf.write("p\3p\3p\3p\7p\u033f\np\fp\16p\u0342\13p\3p\3p\3q\3q\3")
        buf.write("q\3q\6q\u034a\nq\rq\16q\u034b\3r\3r\3s\3s\3s\3t\3t\3t")
        buf.write("\3u\3u\3u\3v\3v\3v\3w\3w\3w\3x\3x\3x\3y\3y\3z\3z\5z\u0366")
        buf.write("\nz\3{\3{\3{\7{\u036b\n{\f{\16{\u036e\13{\3{\3{\3{\3{")
        buf.write("\7{\u0374\n{\f{\16{\u0377\13{\3{\5{\u037a\n{\3|\3|\3|")
        buf.write("\3|\3|\7|\u0381\n|\f|\16|\u0384\13|\3|\3|\3|\3|\3|\3|")
        buf.write("\3|\3|\7|\u038e\n|\f|\16|\u0391\13|\3|\3|\3|\5|\u0396")
        buf.write("\n|\3}\3}\5}\u039a\n}\3~\3~\3\177\3\177\3\177\3\177\5")
        buf.write("\177\u03a2\n\177\5\u01fb\u0382\u038f\2\u0080\3\3\5\4\7")
        buf.write("\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17")
        buf.write("\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63")
        buf.write("\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-")
        buf.write("Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q:s;u\2w<y={>")
        buf.write("}?\177@\u0081A\u0083B\u0085C\u0087D\u0089E\u008bF\u008d")
        buf.write("G\u008fH\u0091I\u0093J\u0095K\u0097L\u0099M\u009bN\u009d")
        buf.write("O\u009fP\u00a1Q\u00a3R\u00a5S\u00a7T\u00a9U\u00abV\u00ad")
        buf.write("W\u00afX\u00b1Y\u00b3Z\u00b5[\u00b7\\\u00b9]\u00bb^\u00bd")
        buf.write("_\u00bf`\u00c1a\u00c3b\u00c5c\u00c7d\u00c9e\u00cbf\u00cd")
        buf.write("g\u00cfh\u00d1i\u00d3j\u00d5k\u00d7l\u00d9m\u00dbn\u00dd")
        buf.write("o\u00dfp\u00e1q\u00e3\2\u00e5r\u00e7s\u00e9t\u00ebu\u00ed")
        buf.write("v\u00efw\u00f1x\u00f3y\u00f5\2\u00f7\2\u00f9\2\u00fb\2")
        buf.write("\u00fd\2\3\2\r\4\2\f\f\16\17\3\2\62;\5\2\62;CHch\3\2\62")
        buf.write("\63\3\2\629\5\2C\\aac|\6\2\62;C\\aac|\3\2\60\60\6\2\f")
        buf.write("\f\16\17))^^\6\2\f\f\16\17$$^^\3\2^^\2\u03be\2\3\3\2\2")
        buf.write("\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2")
        buf.write("\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25")
        buf.write("\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3")
        buf.write("\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2")
        buf.write("\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2")
        buf.write("\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\2")
        buf.write("9\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2")
        buf.write("\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2")
        buf.write("\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2")
        buf.write("\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3")
        buf.write("\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i")
        buf.write("\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2")
        buf.write("s\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2")
        buf.write("\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085")
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
        buf.write("\2\2\u00e1\3\2\2\2\2\u00e5\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9")
        buf.write("\3\2\2\2\2\u00eb\3\2\2\2\2\u00ed\3\2\2\2\2\u00ef\3\2\2")
        buf.write("\2\2\u00f1\3\2\2\2\2\u00f3\3\2\2\2\3\u00ff\3\2\2\2\5\u0103")
        buf.write("\3\2\2\2\7\u0106\3\2\2\2\t\u0108\3\2\2\2\13\u010a\3\2")
        buf.write("\2\2\r\u010c\3\2\2\2\17\u010e\3\2\2\2\21\u0110\3\2\2\2")
        buf.write("\23\u0113\3\2\2\2\25\u0115\3\2\2\2\27\u0117\3\2\2\2\31")
        buf.write("\u011b\3\2\2\2\33\u011e\3\2\2\2\35\u0121\3\2\2\2\37\u0124")
        buf.write("\3\2\2\2!\u0127\3\2\2\2#\u012a\3\2\2\2%\u012c\3\2\2\2")
        buf.write("\'\u012f\3\2\2\2)\u0131\3\2\2\2+\u0134\3\2\2\2-\u0136")
        buf.write("\3\2\2\2/\u0138\3\2\2\2\61\u013a\3\2\2\2\63\u013e\3\2")
        buf.write("\2\2\65\u0146\3\2\2\2\67\u0151\3\2\2\29\u015d\3\2\2\2")
        buf.write(";\u0166\3\2\2\2=\u016a\3\2\2\2?\u016e\3\2\2\2A\u0172\3")
        buf.write("\2\2\2C\u0177\3\2\2\2E\u017b\3\2\2\2G\u017f\3\2\2\2I\u0183")
        buf.write("\3\2\2\2K\u0188\3\2\2\2M\u018d\3\2\2\2O\u0194\3\2\2\2")
        buf.write("Q\u0198\3\2\2\2S\u019d\3\2\2\2U\u01a1\3\2\2\2W\u01a5\3")
        buf.write("\2\2\2Y\u01a8\3\2\2\2[\u01ab\3\2\2\2]\u01ae\3\2\2\2_\u01b1")
        buf.write("\3\2\2\2a\u01b4\3\2\2\2c\u01b7\3\2\2\2e\u01ba\3\2\2\2")
        buf.write("g\u01be\3\2\2\2i\u01c1\3\2\2\2k\u01c6\3\2\2\2m\u01ca\3")
        buf.write("\2\2\2o\u01ce\3\2\2\2q\u01d3\3\2\2\2s\u01f3\3\2\2\2u\u0207")
        buf.write("\3\2\2\2w\u0209\3\2\2\2y\u020b\3\2\2\2{\u020e\3\2\2\2")
        buf.write("}\u0211\3\2\2\2\177\u0213\3\2\2\2\u0081\u0216\3\2\2\2")
        buf.write("\u0083\u0218\3\2\2\2\u0085\u021f\3\2\2\2\u0087\u0225\3")
        buf.write("\2\2\2\u0089\u022a\3\2\2\2\u008b\u022d\3\2\2\2\u008d\u0239")
        buf.write("\3\2\2\2\u008f\u023e\3\2\2\2\u0091\u0243\3\2\2\2\u0093")
        buf.write("\u024a\3\2\2\2\u0095\u024e\3\2\2\2\u0097\u0250\3\2\2\2")
        buf.write("\u0099\u0256\3\2\2\2\u009b\u025c\3\2\2\2\u009d\u0263\3")
        buf.write("\2\2\2\u009f\u0267\3\2\2\2\u00a1\u026c\3\2\2\2\u00a3\u0271")
        buf.write("\3\2\2\2\u00a5\u0275\3\2\2\2\u00a7\u027b\3\2\2\2\u00a9")
        buf.write("\u0283\3\2\2\2\u00ab\u028d\3\2\2\2\u00ad\u0290\3\2\2\2")
        buf.write("\u00af\u0298\3\2\2\2\u00b1\u02a3\3\2\2\2\u00b3\u02a8\3")
        buf.write("\2\2\2\u00b5\u02ac\3\2\2\2\u00b7\u02af\3\2\2\2\u00b9\u02b4")
        buf.write("\3\2\2\2\u00bb\u02b9\3\2\2\2\u00bd\u02bb\3\2\2\2\u00bf")
        buf.write("\u02c1\3\2\2\2\u00c1\u02c5\3\2\2\2\u00c3\u02cd\3\2\2\2")
        buf.write("\u00c5\u02d4\3\2\2\2\u00c7\u02da\3\2\2\2\u00c9\u02dc\3")
        buf.write("\2\2\2\u00cb\u02e2\3\2\2\2\u00cd\u02e5\3\2\2\2\u00cf\u02ea")
        buf.write("\3\2\2\2\u00d1\u02ec\3\2\2\2\u00d3\u02f1\3\2\2\2\u00d5")
        buf.write("\u0305\3\2\2\2\u00d7\u0307\3\2\2\2\u00d9\u032c\3\2\2\2")
        buf.write("\u00db\u032e\3\2\2\2\u00dd\u0335\3\2\2\2\u00df\u033a\3")
        buf.write("\2\2\2\u00e1\u0345\3\2\2\2\u00e3\u034d\3\2\2\2\u00e5\u034f")
        buf.write("\3\2\2\2\u00e7\u0352\3\2\2\2\u00e9\u0355\3\2\2\2\u00eb")
        buf.write("\u0358\3\2\2\2\u00ed\u035b\3\2\2\2\u00ef\u035e\3\2\2\2")
        buf.write("\u00f1\u0361\3\2\2\2\u00f3\u0365\3\2\2\2\u00f5\u0379\3")
        buf.write("\2\2\2\u00f7\u0395\3\2\2\2\u00f9\u0399\3\2\2\2\u00fb\u039b")
        buf.write("\3\2\2\2\u00fd\u03a1\3\2\2\2\u00ff\u0100\7c\2\2\u0100")
        buf.write("\u0101\7p\2\2\u0101\u0102\7f\2\2\u0102\4\3\2\2\2\u0103")
        buf.write("\u0104\7q\2\2\u0104\u0105\7t\2\2\u0105\6\3\2\2\2\u0106")
        buf.write("\u0107\7(\2\2\u0107\b\3\2\2\2\u0108\u0109\7~\2\2\u0109")
        buf.write("\n\3\2\2\2\u010a\u010b\7`\2\2\u010b\f\3\2\2\2\u010c\u010d")
        buf.write("\7/\2\2\u010d\16\3\2\2\2\u010e\u010f\7-\2\2\u010f\20\3")
        buf.write("\2\2\2\u0110\u0111\7\61\2\2\u0111\u0112\7\61\2\2\u0112")
        buf.write("\22\3\2\2\2\u0113\u0114\7\61\2\2\u0114\24\3\2\2\2\u0115")
        buf.write("\u0116\7\'\2\2\u0116\26\3\2\2\2\u0117\u0118\7o\2\2\u0118")
        buf.write("\u0119\7q\2\2\u0119\u011a\7f\2\2\u011a\30\3\2\2\2\u011b")
        buf.write("\u011c\7,\2\2\u011c\u011d\7,\2\2\u011d\32\3\2\2\2\u011e")
        buf.write("\u011f\7>\2\2\u011f\u0120\7>\2\2\u0120\34\3\2\2\2\u0121")
        buf.write("\u0122\7@\2\2\u0122\u0123\7@\2\2\u0123\36\3\2\2\2\u0124")
        buf.write("\u0125\7?\2\2\u0125\u0126\7?\2\2\u0126 \3\2\2\2\u0127")
        buf.write("\u0128\7#\2\2\u0128\u0129\7?\2\2\u0129\"\3\2\2\2\u012a")
        buf.write("\u012b\7>\2\2\u012b$\3\2\2\2\u012c\u012d\7>\2\2\u012d")
        buf.write("\u012e\7?\2\2\u012e&\3\2\2\2\u012f\u0130\7@\2\2\u0130")
        buf.write("(\3\2\2\2\u0131\u0132\7@\2\2\u0132\u0133\7?\2\2\u0133")
        buf.write("*\3\2\2\2\u0134\u0135\7\u0080\2\2\u0135,\3\2\2\2\u0136")
        buf.write("\u0137\7A\2\2\u0137.\3\2\2\2\u0138\u0139\7#\2\2\u0139")
        buf.write("\60\3\2\2\2\u013a\u013b\7c\2\2\u013b\u013c\7d\2\2\u013c")
        buf.write("\u013d\7u\2\2\u013d\62\3\2\2\2\u013e\u013f\7c\2\2\u013f")
        buf.write("\u0140\7v\2\2\u0140\u0141\7N\2\2\u0141\u0142\7c\2\2\u0142")
        buf.write("\u0143\7d\2\2\u0143\u0144\7g\2\2\u0144\u0145\7n\2\2\u0145")
        buf.write("\64\3\2\2\2\u0146\u0147\7e\2\2\u0147\u0148\7q\2\2\u0148")
        buf.write("\u0149\7w\2\2\u0149\u014a\7p\2\2\u014a\u014b\7v\2\2\u014b")
        buf.write("\u014c\7N\2\2\u014c\u014d\7c\2\2\u014d\u014e\7d\2\2\u014e")
        buf.write("\u014f\7g\2\2\u014f\u0150\7n\2\2\u0150\66\3\2\2\2\u0151")
        buf.write("\u0152\7i\2\2\u0152\u0153\7g\2\2\u0153\u0154\7v\2\2\u0154")
        buf.write("\u0155\7a\2\2\u0155\u0156\7e\2\2\u0156\u0157\7q\2\2\u0157")
        buf.write("\u0158\7p\2\2\u0158\u0159\7v\2\2\u0159\u015a\7g\2\2\u015a")
        buf.write("\u015b\7z\2\2\u015b\u015c\7v\2\2\u015c8\3\2\2\2\u015d")
        buf.write("\u015e\7e\2\2\u015e\u015f\7q\2\2\u015f\u0160\7p\2\2\u0160")
        buf.write("\u0161\7v\2\2\u0161\u0162\7g\2\2\u0162\u0163\7z\2\2\u0163")
        buf.write("\u0164\7v\2\2\u0164\u0165\7u\2\2\u0165:\3\2\2\2\u0166")
        buf.write("\u0167\7o\2\2\u0167\u0168\7k\2\2\u0168\u0169\7p\2\2\u0169")
        buf.write("<\3\2\2\2\u016a\u016b\7o\2\2\u016b\u016c\7c\2\2\u016c")
        buf.write("\u016d\7z\2\2\u016d>\3\2\2\2\u016e\u016f\7n\2\2\u016f")
        buf.write("\u0170\7g\2\2\u0170\u0171\7p\2\2\u0171@\3\2\2\2\u0172")
        buf.write("\u0173\7v\2\2\u0173\u0174\7{\2\2\u0174\u0175\7r\2\2\u0175")
        buf.write("\u0176\7g\2\2\u0176B\3\2\2\2\u0177\u0178\7u\2\2\u0178")
        buf.write("\u0179\7v\2\2\u0179\u017a\7t\2\2\u017aD\3\2\2\2\u017b")
        buf.write("\u017c\7c\2\2\u017c\u017d\7p\2\2\u017d\u017e\7{\2\2\u017e")
        buf.write("F\3\2\2\2\u017f\u0180\7c\2\2\u0180\u0181\7n\2\2\u0181")
        buf.write("\u0182\7n\2\2\u0182H\3\2\2\2\u0183\u0184\7m\2\2\u0184")
        buf.write("\u0185\7g\2\2\u0185\u0186\7{\2\2\u0186\u0187\7u\2\2\u0187")
        buf.write("J\3\2\2\2\u0188\u0189\7j\2\2\u0189\u018a\7c\2\2\u018a")
        buf.write("\u018b\7u\2\2\u018b\u018c\7j\2\2\u018cL\3\2\2\2\u018d")
        buf.write("\u018e\7e\2\2\u018e\u018f\7j\2\2\u018f\u0190\7q\2\2\u0190")
        buf.write("\u0191\7q\2\2\u0191\u0192\7u\2\2\u0192\u0193\7g\2\2\u0193")
        buf.write("N\3\2\2\2\u0194\u0195\7g\2\2\u0195\u0196\7p\2\2\u0196")
        buf.write("\u0197\7f\2\2\u0197P\3\2\2\2\u0198\u0199\7c\2\2\u0199")
        buf.write("\u019a\7p\2\2\u019a\u019b\7f\2\2\u019b\u019c\7?\2\2\u019c")
        buf.write("R\3\2\2\2\u019d\u019e\7q\2\2\u019e\u019f\7t\2\2\u019f")
        buf.write("\u01a0\7?\2\2\u01a0T\3\2\2\2\u01a1\u01a2\7?\2\2\u01a2")
        buf.write("\u01a3\7@\2\2\u01a3\u01a4\7?\2\2\u01a4V\3\2\2\2\u01a5")
        buf.write("\u01a6\7(\2\2\u01a6\u01a7\7?\2\2\u01a7X\3\2\2\2\u01a8")
        buf.write("\u01a9\7~\2\2\u01a9\u01aa\7?\2\2\u01aaZ\3\2\2\2\u01ab")
        buf.write("\u01ac\7`\2\2\u01ac\u01ad\7?\2\2\u01ad\\\3\2\2\2\u01ae")
        buf.write("\u01af\7/\2\2\u01af\u01b0\7?\2\2\u01b0^\3\2\2\2\u01b1")
        buf.write("\u01b2\7-\2\2\u01b2\u01b3\7?\2\2\u01b3`\3\2\2\2\u01b4")
        buf.write("\u01b5\7,\2\2\u01b5\u01b6\7?\2\2\u01b6b\3\2\2\2\u01b7")
        buf.write("\u01b8\7\61\2\2\u01b8\u01b9\7?\2\2\u01b9d\3\2\2\2\u01ba")
        buf.write("\u01bb\7\61\2\2\u01bb\u01bc\7\61\2\2\u01bc\u01bd\7?\2")
        buf.write("\2\u01bdf\3\2\2\2\u01be\u01bf\7\'\2\2\u01bf\u01c0\7?\2")
        buf.write("\2\u01c0h\3\2\2\2\u01c1\u01c2\7o\2\2\u01c2\u01c3\7q\2")
        buf.write("\2\u01c3\u01c4\7f\2\2\u01c4\u01c5\7?\2\2\u01c5j\3\2\2")
        buf.write("\2\u01c6\u01c7\7,\2\2\u01c7\u01c8\7,\2\2\u01c8\u01c9\7")
        buf.write("?\2\2\u01c9l\3\2\2\2\u01ca\u01cb\7@\2\2\u01cb\u01cc\7")
        buf.write("@\2\2\u01cc\u01cd\7?\2\2\u01cdn\3\2\2\2\u01ce\u01cf\7")
        buf.write(">\2\2\u01cf\u01d0\7>\2\2\u01d0\u01d1\7?\2\2\u01d1p\3\2")
        buf.write("\2\2\u01d2\u01d4\7\17\2\2\u01d3\u01d2\3\2\2\2\u01d3\u01d4")
        buf.write("\3\2\2\2\u01d4\u01d5\3\2\2\2\u01d5\u01e2\7\f\2\2\u01d6")
        buf.write("\u01d8\7\"\2\2\u01d7\u01d6\3\2\2\2\u01d8\u01db\3\2\2\2")
        buf.write("\u01d9\u01d7\3\2\2\2\u01d9\u01da\3\2\2\2\u01da\u01e3\3")
        buf.write("\2\2\2\u01db\u01d9\3\2\2\2\u01dc\u01de\7\13\2\2\u01dd")
        buf.write("\u01dc\3\2\2\2\u01de\u01e1\3\2\2\2\u01df\u01dd\3\2\2\2")
        buf.write("\u01df\u01e0\3\2\2\2\u01e0\u01e3\3\2\2\2\u01e1\u01df\3")
        buf.write("\2\2\2\u01e2\u01d9\3\2\2\2\u01e2\u01df\3\2\2\2\u01e3\u01e4")
        buf.write("\3\2\2\2\u01e4\u01e5\b9\2\2\u01e5r\3\2\2\2\u01e6\u01e8")
        buf.write("\7\"\2\2\u01e7\u01e6\3\2\2\2\u01e8\u01e9\3\2\2\2\u01e9")
        buf.write("\u01e7\3\2\2\2\u01e9\u01ea\3\2\2\2\u01ea\u01f4\3\2\2\2")
        buf.write("\u01eb\u01ed\7\13\2\2\u01ec\u01eb\3\2\2\2\u01ed\u01ee")
        buf.write("\3\2\2\2\u01ee\u01ec\3\2\2\2\u01ee\u01ef\3\2\2\2\u01ef")
        buf.write("\u01f4\3\2\2\2\u01f0\u01f1\7^\2\2\u01f1\u01f4\5q9\2\u01f2")
        buf.write("\u01f4\5u;\2\u01f3\u01e7\3\2\2\2\u01f3\u01ec\3\2\2\2\u01f3")
        buf.write("\u01f0\3\2\2\2\u01f3\u01f2\3\2\2\2\u01f4\u01f5\3\2\2\2")
        buf.write("\u01f5\u01f6\b:\3\2\u01f6t\3\2\2\2\u01f7\u01fb\5y=\2\u01f8")
        buf.write("\u01fa\13\2\2\2\u01f9\u01f8\3\2\2\2\u01fa\u01fd\3\2\2")
        buf.write("\2\u01fb\u01fc\3\2\2\2\u01fb\u01f9\3\2\2\2\u01fc\u01fe")
        buf.write("\3\2\2\2\u01fd\u01fb\3\2\2\2\u01fe\u01ff\5{>\2\u01ff\u0208")
        buf.write("\3\2\2\2\u0200\u0204\5w<\2\u0201\u0203\n\2\2\2\u0202\u0201")
        buf.write("\3\2\2\2\u0203\u0206\3\2\2\2\u0204\u0202\3\2\2\2\u0204")
        buf.write("\u0205\3\2\2\2\u0205\u0208\3\2\2\2\u0206\u0204\3\2\2\2")
        buf.write("\u0207\u01f7\3\2\2\2\u0207\u0200\3\2\2\2\u0208v\3\2\2")
        buf.write("\2\u0209\u020a\7%\2\2\u020ax\3\2\2\2\u020b\u020c\7*\2")
        buf.write("\2\u020c\u020d\7,\2\2\u020dz\3\2\2\2\u020e\u020f\7,\2")
        buf.write("\2\u020f\u0210\7+\2\2\u0210|\3\2\2\2\u0211\u0212\7,\2")
        buf.write("\2\u0212~\3\2\2\2\u0213\u0214\7c\2\2\u0214\u0215\7u\2")
        buf.write("\2\u0215\u0080\3\2\2\2\u0216\u0217\7\60\2\2\u0217\u0082")
        buf.write("\3\2\2\2\u0218\u0219\7k\2\2\u0219\u021a\7o\2\2\u021a\u021b")
        buf.write("\7r\2\2\u021b\u021c\7q\2\2\u021c\u021d\7t\2\2\u021d\u021e")
        buf.write("\7v\2\2\u021e\u0084\3\2\2\2\u021f\u0220\7r\2\2\u0220\u0221")
        buf.write("\7t\2\2\u0221\u0222\7k\2\2\u0222\u0223\7p\2\2\u0223\u0224")
        buf.write("\7v\2\2\u0224\u0086\3\2\2\2\u0225\u0226\7h\2\2\u0226\u0227")
        buf.write("\7t\2\2\u0227\u0228\7q\2\2\u0228\u0229\7o\2\2\u0229\u0088")
        buf.write("\3\2\2\2\u022a\u022b\7\60\2\2\u022b\u022c\7\60\2\2\u022c")
        buf.write("\u008a\3\2\2\2\u022d\u022e\7u\2\2\u022e\u022f\7g\2\2\u022f")
        buf.write("\u0230\7v\2\2\u0230\u0231\7k\2\2\u0231\u0232\7p\2\2\u0232")
        buf.write("\u0233\7v\2\2\u0233\u0234\7n\2\2\u0234\u0235\7g\2\2\u0235")
        buf.write("\u0236\7x\2\2\u0236\u0237\7g\2\2\u0237\u0238\7n\2\2\u0238")
        buf.write("\u008c\3\2\2\2\u0239\u023a\7u\2\2\u023a\u023b\7c\2\2\u023b")
        buf.write("\u023c\7x\2\2\u023c\u023d\7g\2\2\u023d\u008e\3\2\2\2\u023e")
        buf.write("\u023f\7u\2\2\u023f\u0240\7v\2\2\u0240\u0241\7q\2\2\u0241")
        buf.write("\u0242\7r\2\2\u0242\u0090\3\2\2\2\u0243\u0244\7n\2\2\u0244")
        buf.write("\u0245\7c\2\2\u0245\u0246\7o\2\2\u0246\u0247\7d\2\2\u0247")
        buf.write("\u0248\7f\2\2\u0248\u0249\7c\2\2\u0249\u0092\3\2\2\2\u024a")
        buf.write("\u024b\7p\2\2\u024b\u024c\7q\2\2\u024c\u024d\7v\2\2\u024d")
        buf.write("\u0094\3\2\2\2\u024e\u024f\7.\2\2\u024f\u0096\3\2\2\2")
        buf.write("\u0250\u0251\7e\2\2\u0251\u0252\7q\2\2\u0252\u0253\7p")
        buf.write("\2\2\u0253\u0254\7u\2\2\u0254\u0255\7v\2\2\u0255\u0098")
        buf.write("\3\2\2\2\u0256\u0257\7c\2\2\u0257\u0258\7y\2\2\u0258\u0259")
        buf.write("\7c\2\2\u0259\u025a\7k\2\2\u025a\u025b\7v\2\2\u025b\u009a")
        buf.write("\3\2\2\2\u025c\u025d\7c\2\2\u025d\u025e\7u\2\2\u025e\u025f")
        buf.write("\7u\2\2\u025f\u0260\7g\2\2\u0260\u0261\7t\2\2\u0261\u0262")
        buf.write("\7v\2\2\u0262\u009c\3\2\2\2\u0263\u0264\7x\2\2\u0264\u0265")
        buf.write("\7c\2\2\u0265\u0266\7t\2\2\u0266\u009e\3\2\2\2\u0267\u0268")
        buf.write("\7v\2\2\u0268\u0269\7t\2\2\u0269\u026a\7c\2\2\u026a\u026b")
        buf.write("\7r\2\2\u026b\u00a0\3\2\2\2\u026c\u026d\7r\2\2\u026d\u026e")
        buf.write("\7c\2\2\u026e\u026f\7u\2\2\u026f\u0270\7u\2\2\u0270\u00a2")
        buf.write("\3\2\2\2\u0271\u0272\7f\2\2\u0272\u0273\7g\2\2\u0273\u0274")
        buf.write("\7n\2\2\u0274\u00a4\3\2\2\2\u0275\u0276\7u\2\2\u0276\u0277")
        buf.write("\7r\2\2\u0277\u0278\7c\2\2\u0278\u0279\7y\2\2\u0279\u027a")
        buf.write("\7p\2\2\u027a\u00a6\3\2\2\2\u027b\u027c\7h\2\2\u027c\u027d")
        buf.write("\7k\2\2\u027d\u027e\7p\2\2\u027e\u027f\7c\2\2\u027f\u0280")
        buf.write("\7n\2\2\u0280\u0281\7n\2\2\u0281\u0282\7{\2\2\u0282\u00a8")
        buf.write("\3\2\2\2\u0283\u0284\7k\2\2\u0284\u0285\7p\2\2\u0285\u0286")
        buf.write("\7x\2\2\u0286\u0287\7c\2\2\u0287\u0288\7t\2\2\u0288\u0289")
        buf.write("\7k\2\2\u0289\u028a\7c\2\2\u028a\u028b\7p\2\2\u028b\u028c")
        buf.write("\7v\2\2\u028c\u00aa\3\2\2\2\u028d\u028e\7i\2\2\u028e\u028f")
        buf.write("\7q\2\2\u028f\u00ac\3\2\2\2\u0290\u0291\7d\2\2\u0291\u0292")
        buf.write("\7w\2\2\u0292\u0293\7k\2\2\u0293\u0294\7n\2\2\u0294\u0295")
        buf.write("\7v\2\2\u0295\u0296\7k\2\2\u0296\u0297\7p\2\2\u0297\u00ae")
        buf.write("\3\2\2\2\u0298\u0299\7u\2\2\u0299\u029a\7g\2\2\u029a\u029b")
        buf.write("\7s\2\2\u029b\u029c\7w\2\2\u029c\u029d\7g\2\2\u029d\u029e")
        buf.write("\7p\2\2\u029e\u029f\7v\2\2\u029f\u02a0\7k\2\2\u02a0\u02a1")
        buf.write("\7c\2\2\u02a1\u02a2\7n\2\2\u02a2\u00b0\3\2\2\2\u02a3\u02a4")
        buf.write("\7y\2\2\u02a4\u02a5\7j\2\2\u02a5\u02a6\7g\2\2\u02a6\u02a7")
        buf.write("\7p\2\2\u02a7\u00b2\3\2\2\2\u02a8\u02a9\7n\2\2\u02a9\u02aa")
        buf.write("\7g\2\2\u02aa\u02ab\7v\2\2\u02ab\u00b4\3\2\2\2\u02ac\u02ad")
        buf.write("\7k\2\2\u02ad\u02ae\7h\2\2\u02ae\u00b6\3\2\2\2\u02af\u02b0")
        buf.write("\7g\2\2\u02b0\u02b1\7n\2\2\u02b1\u02b2\7k\2\2\u02b2\u02b3")
        buf.write("\7h\2\2\u02b3\u00b8\3\2\2\2\u02b4\u02b5\7g\2\2\u02b5\u02b6")
        buf.write("\7n\2\2\u02b6\u02b7\7u\2\2\u02b7\u02b8\7g\2\2\u02b8\u00ba")
        buf.write("\3\2\2\2\u02b9\u02ba\7B\2\2\u02ba\u00bc\3\2\2\2\u02bb")
        buf.write("\u02bc\7y\2\2\u02bc\u02bd\7j\2\2\u02bd\u02be\7k\2\2\u02be")
        buf.write("\u02bf\7n\2\2\u02bf\u02c0\7g\2\2\u02c0\u00be\3\2\2\2\u02c1")
        buf.write("\u02c2\7f\2\2\u02c2\u02c3\7g\2\2\u02c3\u02c4\7h\2\2\u02c4")
        buf.write("\u00c0\3\2\2\2\u02c5\u02c6\7t\2\2\u02c6\u02c7\7g\2\2\u02c7")
        buf.write("\u02c8\7v\2\2\u02c8\u02c9\7w\2\2\u02c9\u02ca\7t\2\2\u02ca")
        buf.write("\u02cb\7p\2\2\u02cb\u02cc\7u\2\2\u02cc\u00c2\3\2\2\2\u02cd")
        buf.write("\u02ce\7g\2\2\u02ce\u02cf\7z\2\2\u02cf\u02d0\7k\2\2\u02d0")
        buf.write("\u02d1\7u\2\2\u02d1\u02d2\7v\2\2\u02d2\u02d3\7u\2\2\u02d3")
        buf.write("\u00c4\3\2\2\2\u02d4\u02d5\7y\2\2\u02d5\u02d6\7j\2\2\u02d6")
        buf.write("\u02d7\7g\2\2\u02d7\u02d8\7t\2\2\u02d8\u02d9\7g\2\2\u02d9")
        buf.write("\u00c6\3\2\2\2\u02da\u02db\7?\2\2\u02db\u00c8\3\2\2\2")
        buf.write("\u02dc\u02dd\7h\2\2\u02dd\u02de\7q\2\2\u02de\u02df\7t")
        buf.write("\2\2\u02df\u02e0\3\2\2\2\u02e0\u02e1\be\4\2\u02e1\u00ca")
        buf.write("\3\2\2\2\u02e2\u02e3\7?\2\2\u02e3\u02e4\7@\2\2\u02e4\u00cc")
        buf.write("\3\2\2\2\u02e5\u02e6\7k\2\2\u02e6\u02e7\7p\2\2\u02e7\u02e8")
        buf.write("\3\2\2\2\u02e8\u02e9\bg\5\2\u02e9\u00ce\3\2\2\2\u02ea")
        buf.write("\u02eb\7<\2\2\u02eb\u00d0\3\2\2\2\u02ec\u02ed\7P\2\2\u02ed")
        buf.write("\u02ee\7q\2\2\u02ee\u02ef\7p\2\2\u02ef\u02f0\7g\2\2\u02f0")
        buf.write("\u00d2\3\2\2\2\u02f1\u02f2\7c\2\2\u02f2\u02f3\7v\2\2\u02f3")
        buf.write("\u02f4\7q\2\2\u02f4\u02f5\7o\2\2\u02f5\u02f6\7k\2\2\u02f6")
        buf.write("\u02f7\7e\2\2\u02f7\u02f8\7c\2\2\u02f8\u02f9\7n\2\2\u02f9")
        buf.write("\u02fa\7n\2\2\u02fa\u02fb\7{\2\2\u02fb\u00d4\3\2\2\2\u02fc")
        buf.write("\u02fd\7H\2\2\u02fd\u02fe\7c\2\2\u02fe\u02ff\7n\2\2\u02ff")
        buf.write("\u0300\7u\2\2\u0300\u0306\7g\2\2\u0301\u0302\7V\2\2\u0302")
        buf.write("\u0303\7t\2\2\u0303\u0304\7w\2\2\u0304\u0306\7g\2\2\u0305")
        buf.write("\u02fc\3\2\2\2\u0305\u0301\3\2\2\2\u0306\u00d6\3\2\2\2")
        buf.write("\u0307\u0308\7g\2\2\u0308\u0309\7v\2\2\u0309\u030a\7g")
        buf.write("\2\2\u030a\u030b\7t\2\2\u030b\u030c\7p\2\2\u030c\u030d")
        buf.write("\7c\2\2\u030d\u030e\7n\2\2\u030e\u00d8\3\2\2\2\u030f\u0311")
        buf.write("\t\3\2\2\u0310\u030f\3\2\2\2\u0311\u0312\3\2\2\2\u0312")
        buf.write("\u0310\3\2\2\2\u0312\u0313\3\2\2\2\u0313\u032d\3\2\2\2")
        buf.write("\u0314\u0315\7\62\2\2\u0315\u0316\7z\2\2\u0316\u0318\3")
        buf.write("\2\2\2\u0317\u0319\t\4\2\2\u0318\u0317\3\2\2\2\u0319\u031a")
        buf.write("\3\2\2\2\u031a\u0318\3\2\2\2\u031a\u031b\3\2\2\2\u031b")
        buf.write("\u032d\3\2\2\2\u031c\u031d\7\62\2\2\u031d\u031e\7d\2\2")
        buf.write("\u031e\u0320\3\2\2\2\u031f\u0321\t\5\2\2\u0320\u031f\3")
        buf.write("\2\2\2\u0321\u0322\3\2\2\2\u0322\u0320\3\2\2\2\u0322\u0323")
        buf.write("\3\2\2\2\u0323\u032d\3\2\2\2\u0324\u0325\7\62\2\2\u0325")
        buf.write("\u0326\7q\2\2\u0326\u0328\3\2\2\2\u0327\u0329\t\6\2\2")
        buf.write("\u0328\u0327\3\2\2\2\u0329\u032a\3\2\2\2\u032a\u0328\3")
        buf.write("\2\2\2\u032a\u032b\3\2\2\2\u032b\u032d\3\2\2\2\u032c\u0310")
        buf.write("\3\2\2\2\u032c\u0314\3\2\2\2\u032c\u031c\3\2\2\2\u032c")
        buf.write("\u0324\3\2\2\2\u032d\u00da\3\2\2\2\u032e\u0332\t\7\2\2")
        buf.write("\u032f\u0331\t\b\2\2\u0330\u032f\3\2\2\2\u0331\u0334\3")
        buf.write("\2\2\2\u0332\u0330\3\2\2\2\u0332\u0333\3\2\2\2\u0333\u00dc")
        buf.write("\3\2\2\2\u0334\u0332\3\2\2\2\u0335\u0338\t\t\2\2\u0336")
        buf.write("\u0339\5\u00e1q\2\u0337\u0339\5\u00dbn\2\u0338\u0336\3")
        buf.write("\2\2\2\u0338\u0337\3\2\2\2\u0339\u00de\3\2\2\2\u033a\u033b")
        buf.write("\7/\2\2\u033b\u033c\7@\2\2\u033c\u0340\3\2\2\2\u033d\u033f")
        buf.write("\7\"\2\2\u033e\u033d\3\2\2\2\u033f\u0342\3\2\2\2\u0340")
        buf.write("\u033e\3\2\2\2\u0340\u0341\3\2\2\2\u0341\u0343\3\2\2\2")
        buf.write("\u0342\u0340\3\2\2\2\u0343\u0344\5\u00dbn\2\u0344\u00e0")
        buf.write("\3\2\2\2\u0345\u0346\7\62\2\2\u0346\u0347\7Z\2\2\u0347")
        buf.write("\u0349\3\2\2\2\u0348\u034a\5\u00e3r\2\u0349\u0348\3\2")
        buf.write("\2\2\u034a\u034b\3\2\2\2\u034b\u0349\3\2\2\2\u034b\u034c")
        buf.write("\3\2\2\2\u034c\u00e2\3\2\2\2\u034d\u034e\t\4\2\2\u034e")
        buf.write("\u00e4\3\2\2\2\u034f\u0350\7]\2\2\u0350\u0351\bs\6\2\u0351")
        buf.write("\u00e6\3\2\2\2\u0352\u0353\7_\2\2\u0353\u0354\bt\7\2\u0354")
        buf.write("\u00e8\3\2\2\2\u0355\u0356\7}\2\2\u0356\u0357\bu\b\2\u0357")
        buf.write("\u00ea\3\2\2\2\u0358\u0359\7\177\2\2\u0359\u035a\bv\t")
        buf.write("\2\u035a\u00ec\3\2\2\2\u035b\u035c\7*\2\2\u035c\u035d")
        buf.write("\bw\n\2\u035d\u00ee\3\2\2\2\u035e\u035f\7+\2\2\u035f\u0360")
        buf.write("\bx\13\2\u0360\u00f0\3\2\2\2\u0361\u0362\7=\2\2\u0362")
        buf.write("\u00f2\3\2\2\2\u0363\u0366\5\u00f5{\2\u0364\u0366\5\u00f7")
        buf.write("|\2\u0365\u0363\3\2\2\2\u0365\u0364\3\2\2\2\u0366\u00f4")
        buf.write("\3\2\2\2\u0367\u036c\7)\2\2\u0368\u036b\5\u00fd\177\2")
        buf.write("\u0369\u036b\n\n\2\2\u036a\u0368\3\2\2\2\u036a\u0369\3")
        buf.write("\2\2\2\u036b\u036e\3\2\2\2\u036c\u036a\3\2\2\2\u036c\u036d")
        buf.write("\3\2\2\2\u036d\u036f\3\2\2\2\u036e\u036c\3\2\2\2\u036f")
        buf.write("\u037a\7)\2\2\u0370\u0375\7$\2\2\u0371\u0374\5\u00fd\177")
        buf.write("\2\u0372\u0374\n\13\2\2\u0373\u0371\3\2\2\2\u0373\u0372")
        buf.write("\3\2\2\2\u0374\u0377\3\2\2\2\u0375\u0373\3\2\2\2\u0375")
        buf.write("\u0376\3\2\2\2\u0376\u0378\3\2\2\2\u0377\u0375\3\2\2\2")
        buf.write("\u0378\u037a\7$\2\2\u0379\u0367\3\2\2\2\u0379\u0370\3")
        buf.write("\2\2\2\u037a\u00f6\3\2\2\2\u037b\u037c\7)\2\2\u037c\u037d")
        buf.write("\7)\2\2\u037d\u037e\7)\2\2\u037e\u0382\3\2\2\2\u037f\u0381")
        buf.write("\5\u00f9}\2\u0380\u037f\3\2\2\2\u0381\u0384\3\2\2\2\u0382")
        buf.write("\u0383\3\2\2\2\u0382\u0380\3\2\2\2\u0383\u0385\3\2\2\2")
        buf.write("\u0384\u0382\3\2\2\2\u0385\u0386\7)\2\2\u0386\u0387\7")
        buf.write(")\2\2\u0387\u0396\7)\2\2\u0388\u0389\7$\2\2\u0389\u038a")
        buf.write("\7$\2\2\u038a\u038b\7$\2\2\u038b\u038f\3\2\2\2\u038c\u038e")
        buf.write("\5\u00f9}\2\u038d\u038c\3\2\2\2\u038e\u0391\3\2\2\2\u038f")
        buf.write("\u0390\3\2\2\2\u038f\u038d\3\2\2\2\u0390\u0392\3\2\2\2")
        buf.write("\u0391\u038f\3\2\2\2\u0392\u0393\7$\2\2\u0393\u0394\7")
        buf.write("$\2\2\u0394\u0396\7$\2\2\u0395\u037b\3\2\2\2\u0395\u0388")
        buf.write("\3\2\2\2\u0396\u00f8\3\2\2\2\u0397\u039a\5\u00fb~\2\u0398")
        buf.write("\u039a\5\u00fd\177\2\u0399\u0397\3\2\2\2\u0399\u0398\3")
        buf.write("\2\2\2\u039a\u00fa\3\2\2\2\u039b\u039c\n\f\2\2\u039c\u00fc")
        buf.write("\3\2\2\2\u039d\u039e\7^\2\2\u039e\u03a2\13\2\2\2\u039f")
        buf.write("\u03a0\7^\2\2\u03a0\u03a2\5q9\2\u03a1\u039d\3\2\2\2\u03a1")
        buf.write("\u039f\3\2\2\2\u03a2\u00fe\3\2\2\2\"\2\u01d3\u01d9\u01df")
        buf.write("\u01e2\u01e9\u01ee\u01f3\u01fb\u0204\u0207\u0305\u0312")
        buf.write("\u031a\u0322\u032a\u032c\u0332\u0338\u0340\u034b\u0365")
        buf.write("\u036a\u036c\u0373\u0375\u0379\u0382\u038f\u0395\u0399")
        buf.write("\u03a1\f\39\2\b\2\2\3e\3\3g\4\3s\5\3t\6\3u\7\3v\b\3w\t")
        buf.write("\3x\n")
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
    DEF = 94
    RETURNS = 95
    EXISTS = 96
    WHERE = 97
    EQ = 98
    FOR = 99
    IMPLIES = 100
    IN = 101
    COLON = 102
    NONE = 103
    ATOMICALLY = 104
    BOOL = 105
    ETERNAL = 106
    INT = 107
    NAME = 108
    ATOM = 109
    ARROWID = 110
    HEX_INTEGER = 111
    OPEN_BRACK = 112
    CLOSE_BRACK = 113
    OPEN_BRACES = 114
    CLOSE_BRACES = 115
    OPEN_PAREN = 116
    CLOSE_PAREN = 117
    SEMI_COLON = 118
    STRING = 119

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
            "'else'", "'@'", "'while'", "'def'", "'returns'", "'exists'", 
            "'where'", "'='", "'for'", "'=>'", "'in'", "':'", "'None'", 
            "'atomically'", "'eternal'", "'['", "']'", "'{'", "'}'", "'('", 
            "')'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "NL", "WS", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
            "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", "RANGE", "SETINTLEVEL", 
            "SAVE", "STOP", "LAMBDA", "NOT", "COMMA", "CONST", "AWAIT", 
            "ASSERT", "VAR", "TRAP", "PASS", "DEL", "SPAWN", "FINALLY", 
            "INVARIANT", "GO", "BUILTIN", "SEQUENTIAL", "WHEN", "LET", "IF", 
            "ELIF", "ELSE", "AT", "WHILE", "DEF", "RETURNS", "EXISTS", "WHERE", 
            "EQ", "FOR", "IMPLIES", "IN", "COLON", "NONE", "ATOMICALLY", 
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
                  "WHEN", "LET", "IF", "ELIF", "ELSE", "AT", "WHILE", "DEF", 
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
            actions[55] = self.NL_action 
            actions[99] = self.FOR_action 
            actions[101] = self.IN_action 
            actions[113] = self.OPEN_BRACK_action 
            actions[114] = self.CLOSE_BRACK_action 
            actions[115] = self.OPEN_BRACES_action 
            actions[116] = self.CLOSE_BRACES_action 
            actions[117] = self.OPEN_PAREN_action 
            actions[118] = self.CLOSE_PAREN_action 
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
     


