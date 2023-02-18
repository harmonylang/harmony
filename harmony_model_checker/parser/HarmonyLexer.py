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
        buf.write("\u039b\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3")
        buf.write("\7\3\b\3\b\3\t\3\t\3\n\3\n\3\n\3\13\3\13\3\f\3\f\3\r\3")
        buf.write("\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3\17\3\20\3\20\3\20")
        buf.write("\3\21\3\21\3\21\3\22\3\22\3\22\3\23\3\23\3\24\3\24\3\24")
        buf.write("\3\25\3\25\3\26\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31")
        buf.write("\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\33\3\33\3\33")
        buf.write("\3\33\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3!\3!\3!\3!\3\"\3\"\3")
        buf.write("\"\3\"\3\"\3#\3#\3#\3#\3$\3$\3$\3$\3%\3%\3%\3%\3&\3&\3")
        buf.write("&\3&\3&\3\'\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3(\3(\3(\3)\3")
        buf.write(")\3)\3)\3*\3*\3*\3*\3*\3+\3+\3+\3+\3,\3,\3,\3,\3-\3-\3")
        buf.write("-\3.\3.\3.\3/\3/\3/\3\60\3\60\3\60\3\61\3\61\3\61\3\62")
        buf.write("\3\62\3\62\3\63\3\63\3\63\3\64\3\64\3\64\3\64\3\65\3\65")
        buf.write("\3\65\3\66\3\66\3\66\3\66\3\66\3\67\3\67\3\67\3\67\38")
        buf.write("\38\38\38\39\39\39\39\3:\5:\u01d7\n:\3:\3:\7:\u01db\n")
        buf.write(":\f:\16:\u01de\13:\3:\7:\u01e1\n:\f:\16:\u01e4\13:\5:")
        buf.write("\u01e6\n:\3:\3:\3;\6;\u01eb\n;\r;\16;\u01ec\3;\6;\u01f0")
        buf.write("\n;\r;\16;\u01f1\3;\3;\3;\5;\u01f7\n;\3;\3;\3<\3<\7<\u01fd")
        buf.write("\n<\f<\16<\u0200\13<\3<\3<\3<\3<\7<\u0206\n<\f<\16<\u0209")
        buf.write("\13<\5<\u020b\n<\3=\3=\3>\3>\3>\3?\3?\3?\3@\3@\3A\3A\3")
        buf.write("A\3B\3B\3C\3C\3C\3C\3C\3C\3C\3D\3D\3D\3D\3D\3D\3E\3E\3")
        buf.write("E\3E\3E\3F\3F\3F\3G\3G\3G\3G\3G\3G\3G\3G\3G\3G\3G\3G\3")
        buf.write("H\3H\3H\3I\3I\3I\3I\3I\3J\3J\3J\3J\3J\3K\3K\3K\3K\3K\3")
        buf.write("K\3K\3L\3L\3L\3L\3M\3M\3N\3N\3N\3N\3N\3N\3O\3O\3O\3O\3")
        buf.write("O\3O\3P\3P\3P\3P\3P\3P\3P\3Q\3Q\3Q\3Q\3R\3R\3R\3R\3R\3")
        buf.write("S\3S\3S\3S\3S\3T\3T\3T\3T\3U\3U\3U\3U\3U\3U\3V\3V\3V\3")
        buf.write("V\3V\3V\3V\3V\3W\3W\3W\3W\3W\3W\3W\3W\3W\3W\3X\3X\3X\3")
        buf.write("Y\3Y\3Y\3Y\3Y\3Y\3Y\3Y\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3")
        buf.write("Z\3[\3[\3[\3[\3[\3\\\3\\\3\\\3\\\3]\3]\3]\3^\3^\3^\3^")
        buf.write("\3^\3_\3_\3_\3_\3_\3`\3`\3a\3a\3a\3a\3a\3a\3b\3b\3b\3")
        buf.write("b\3c\3c\3c\3c\3c\3c\3c\3c\3d\3d\3d\3d\3d\3d\3d\3e\3e\3")
        buf.write("e\3e\3e\3e\3f\3f\3g\3g\3g\3g\3g\3g\3h\3h\3h\3h\3h\3i\3")
        buf.write("i\3j\3j\3j\3j\3j\3k\3k\3k\3k\3k\3k\3k\3k\3k\3k\3k\3l\3")
        buf.write("l\3l\3l\3l\3l\3l\3l\3l\5l\u0309\nl\3m\3m\3m\3m\3m\3m\3")
        buf.write("m\3m\3n\6n\u0314\nn\rn\16n\u0315\3n\3n\3n\3n\6n\u031c")
        buf.write("\nn\rn\16n\u031d\3n\3n\3n\3n\6n\u0324\nn\rn\16n\u0325")
        buf.write("\3n\3n\3n\3n\6n\u032c\nn\rn\16n\u032d\5n\u0330\nn\3o\3")
        buf.write("o\7o\u0334\no\fo\16o\u0337\13o\3p\3p\3p\5p\u033c\np\3")
        buf.write("q\3q\3q\3q\6q\u0342\nq\rq\16q\u0343\3r\3r\3s\3s\3s\3t")
        buf.write("\3t\3t\3u\3u\3u\3v\3v\3v\3w\3w\3w\3x\3x\3x\3y\3y\3z\3")
        buf.write("z\5z\u035e\nz\3{\3{\3{\7{\u0363\n{\f{\16{\u0366\13{\3")
        buf.write("{\3{\3{\3{\7{\u036c\n{\f{\16{\u036f\13{\3{\5{\u0372\n")
        buf.write("{\3|\3|\3|\3|\3|\7|\u0379\n|\f|\16|\u037c\13|\3|\3|\3")
        buf.write("|\3|\3|\3|\3|\3|\7|\u0386\n|\f|\16|\u0389\13|\3|\3|\3")
        buf.write("|\5|\u038e\n|\3}\3}\5}\u0392\n}\3~\3~\3\177\3\177\3\177")
        buf.write("\3\177\5\177\u039a\n\177\5\u01fe\u037a\u0387\2\u0080\3")
        buf.write("\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16")
        buf.write("\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61")
        buf.write("\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*")
        buf.write("S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q:s;u<w")
        buf.write("\2y={>}?\177@\u0081A\u0083B\u0085C\u0087D\u0089E\u008b")
        buf.write("F\u008dG\u008fH\u0091I\u0093J\u0095K\u0097L\u0099M\u009b")
        buf.write("N\u009dO\u009fP\u00a1Q\u00a3R\u00a5S\u00a7T\u00a9U\u00ab")
        buf.write("V\u00adW\u00afX\u00b1Y\u00b3Z\u00b5[\u00b7\\\u00b9]\u00bb")
        buf.write("^\u00bd_\u00bf`\u00c1a\u00c3b\u00c5c\u00c7d\u00c9e\u00cb")
        buf.write("f\u00cdg\u00cfh\u00d1i\u00d3j\u00d5k\u00d7l\u00d9m\u00db")
        buf.write("n\u00ddo\u00dfp\u00e1q\u00e3\2\u00e5r\u00e7s\u00e9t\u00eb")
        buf.write("u\u00edv\u00efw\u00f1x\u00f3y\u00f5\2\u00f7\2\u00f9\2")
        buf.write("\u00fb\2\u00fd\2\3\2\r\4\2\f\f\16\17\3\2\62;\5\2\62;C")
        buf.write("Hch\3\2\62\63\3\2\629\5\2C\\aac|\6\2\62;C\\aac|\3\2\60")
        buf.write("\60\6\2\f\f\16\17))^^\6\2\f\f\16\17$$^^\3\2^^\2\u03b5")
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
        buf.write("\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2")
        buf.write("}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2")
        buf.write("\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2\u008b")
        buf.write("\3\2\2\2\2\u008d\3\2\2\2\2\u008f\3\2\2\2\2\u0091\3\2\2")
        buf.write("\2\2\u0093\3\2\2\2\2\u0095\3\2\2\2\2\u0097\3\2\2\2\2\u0099")
        buf.write("\3\2\2\2\2\u009b\3\2\2\2\2\u009d\3\2\2\2\2\u009f\3\2\2")
        buf.write("\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2\2\2\u00a5\3\2\2\2\2\u00a7")
        buf.write("\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab\3\2\2\2\2\u00ad\3\2\2")
        buf.write("\2\2\u00af\3\2\2\2\2\u00b1\3\2\2\2\2\u00b3\3\2\2\2\2\u00b5")
        buf.write("\3\2\2\2\2\u00b7\3\2\2\2\2\u00b9\3\2\2\2\2\u00bb\3\2\2")
        buf.write("\2\2\u00bd\3\2\2\2\2\u00bf\3\2\2\2\2\u00c1\3\2\2\2\2\u00c3")
        buf.write("\3\2\2\2\2\u00c5\3\2\2\2\2\u00c7\3\2\2\2\2\u00c9\3\2\2")
        buf.write("\2\2\u00cb\3\2\2\2\2\u00cd\3\2\2\2\2\u00cf\3\2\2\2\2\u00d1")
        buf.write("\3\2\2\2\2\u00d3\3\2\2\2\2\u00d5\3\2\2\2\2\u00d7\3\2\2")
        buf.write("\2\2\u00d9\3\2\2\2\2\u00db\3\2\2\2\2\u00dd\3\2\2\2\2\u00df")
        buf.write("\3\2\2\2\2\u00e1\3\2\2\2\2\u00e5\3\2\2\2\2\u00e7\3\2\2")
        buf.write("\2\2\u00e9\3\2\2\2\2\u00eb\3\2\2\2\2\u00ed\3\2\2\2\2\u00ef")
        buf.write("\3\2\2\2\2\u00f1\3\2\2\2\2\u00f3\3\2\2\2\3\u00ff\3\2\2")
        buf.write("\2\5\u0103\3\2\2\2\7\u0106\3\2\2\2\t\u0109\3\2\2\2\13")
        buf.write("\u010b\3\2\2\2\r\u010d\3\2\2\2\17\u010f\3\2\2\2\21\u0111")
        buf.write("\3\2\2\2\23\u0113\3\2\2\2\25\u0116\3\2\2\2\27\u0118\3")
        buf.write("\2\2\2\31\u011a\3\2\2\2\33\u011e\3\2\2\2\35\u0121\3\2")
        buf.write("\2\2\37\u0124\3\2\2\2!\u0127\3\2\2\2#\u012a\3\2\2\2%\u012d")
        buf.write("\3\2\2\2\'\u012f\3\2\2\2)\u0132\3\2\2\2+\u0134\3\2\2\2")
        buf.write("-\u0137\3\2\2\2/\u0139\3\2\2\2\61\u013b\3\2\2\2\63\u013d")
        buf.write("\3\2\2\2\65\u0141\3\2\2\2\67\u0149\3\2\2\29\u0154\3\2")
        buf.write("\2\2;\u0160\3\2\2\2=\u0169\3\2\2\2?\u016d\3\2\2\2A\u0171")
        buf.write("\3\2\2\2C\u0175\3\2\2\2E\u017a\3\2\2\2G\u017e\3\2\2\2")
        buf.write("I\u0182\3\2\2\2K\u0186\3\2\2\2M\u018b\3\2\2\2O\u0190\3")
        buf.write("\2\2\2Q\u0197\3\2\2\2S\u019b\3\2\2\2U\u01a0\3\2\2\2W\u01a4")
        buf.write("\3\2\2\2Y\u01a8\3\2\2\2[\u01ab\3\2\2\2]\u01ae\3\2\2\2")
        buf.write("_\u01b1\3\2\2\2a\u01b4\3\2\2\2c\u01b7\3\2\2\2e\u01ba\3")
        buf.write("\2\2\2g\u01bd\3\2\2\2i\u01c1\3\2\2\2k\u01c4\3\2\2\2m\u01c9")
        buf.write("\3\2\2\2o\u01cd\3\2\2\2q\u01d1\3\2\2\2s\u01d6\3\2\2\2")
        buf.write("u\u01f6\3\2\2\2w\u020a\3\2\2\2y\u020c\3\2\2\2{\u020e\3")
        buf.write("\2\2\2}\u0211\3\2\2\2\177\u0214\3\2\2\2\u0081\u0216\3")
        buf.write("\2\2\2\u0083\u0219\3\2\2\2\u0085\u021b\3\2\2\2\u0087\u0222")
        buf.write("\3\2\2\2\u0089\u0228\3\2\2\2\u008b\u022d\3\2\2\2\u008d")
        buf.write("\u0230\3\2\2\2\u008f\u023c\3\2\2\2\u0091\u023f\3\2\2\2")
        buf.write("\u0093\u0244\3\2\2\2\u0095\u0249\3\2\2\2\u0097\u0250\3")
        buf.write("\2\2\2\u0099\u0254\3\2\2\2\u009b\u0256\3\2\2\2\u009d\u025c")
        buf.write("\3\2\2\2\u009f\u0262\3\2\2\2\u00a1\u0269\3\2\2\2\u00a3")
        buf.write("\u026d\3\2\2\2\u00a5\u0272\3\2\2\2\u00a7\u0277\3\2\2\2")
        buf.write("\u00a9\u027b\3\2\2\2\u00ab\u0281\3\2\2\2\u00ad\u0289\3")
        buf.write("\2\2\2\u00af\u0293\3\2\2\2\u00b1\u0296\3\2\2\2\u00b3\u029e")
        buf.write("\3\2\2\2\u00b5\u02a9\3\2\2\2\u00b7\u02ae\3\2\2\2\u00b9")
        buf.write("\u02b2\3\2\2\2\u00bb\u02b5\3\2\2\2\u00bd\u02ba\3\2\2\2")
        buf.write("\u00bf\u02bf\3\2\2\2\u00c1\u02c1\3\2\2\2\u00c3\u02c7\3")
        buf.write("\2\2\2\u00c5\u02cb\3\2\2\2\u00c7\u02d3\3\2\2\2\u00c9\u02da")
        buf.write("\3\2\2\2\u00cb\u02e0\3\2\2\2\u00cd\u02e2\3\2\2\2\u00cf")
        buf.write("\u02e8\3\2\2\2\u00d1\u02ed\3\2\2\2\u00d3\u02ef\3\2\2\2")
        buf.write("\u00d5\u02f4\3\2\2\2\u00d7\u0308\3\2\2\2\u00d9\u030a\3")
        buf.write("\2\2\2\u00db\u032f\3\2\2\2\u00dd\u0331\3\2\2\2\u00df\u0338")
        buf.write("\3\2\2\2\u00e1\u033d\3\2\2\2\u00e3\u0345\3\2\2\2\u00e5")
        buf.write("\u0347\3\2\2\2\u00e7\u034a\3\2\2\2\u00e9\u034d\3\2\2\2")
        buf.write("\u00eb\u0350\3\2\2\2\u00ed\u0353\3\2\2\2\u00ef\u0356\3")
        buf.write("\2\2\2\u00f1\u0359\3\2\2\2\u00f3\u035d\3\2\2\2\u00f5\u0371")
        buf.write("\3\2\2\2\u00f7\u038d\3\2\2\2\u00f9\u0391\3\2\2\2\u00fb")
        buf.write("\u0393\3\2\2\2\u00fd\u0399\3\2\2\2\u00ff\u0100\7c\2\2")
        buf.write("\u0100\u0101\7p\2\2\u0101\u0102\7f\2\2\u0102\4\3\2\2\2")
        buf.write("\u0103\u0104\7q\2\2\u0104\u0105\7t\2\2\u0105\6\3\2\2\2")
        buf.write("\u0106\u0107\7?\2\2\u0107\u0108\7@\2\2\u0108\b\3\2\2\2")
        buf.write("\u0109\u010a\7(\2\2\u010a\n\3\2\2\2\u010b\u010c\7~\2\2")
        buf.write("\u010c\f\3\2\2\2\u010d\u010e\7`\2\2\u010e\16\3\2\2\2\u010f")
        buf.write("\u0110\7/\2\2\u0110\20\3\2\2\2\u0111\u0112\7-\2\2\u0112")
        buf.write("\22\3\2\2\2\u0113\u0114\7\61\2\2\u0114\u0115\7\61\2\2")
        buf.write("\u0115\24\3\2\2\2\u0116\u0117\7\61\2\2\u0117\26\3\2\2")
        buf.write("\2\u0118\u0119\7\'\2\2\u0119\30\3\2\2\2\u011a\u011b\7")
        buf.write("o\2\2\u011b\u011c\7q\2\2\u011c\u011d\7f\2\2\u011d\32\3")
        buf.write("\2\2\2\u011e\u011f\7,\2\2\u011f\u0120\7,\2\2\u0120\34")
        buf.write("\3\2\2\2\u0121\u0122\7>\2\2\u0122\u0123\7>\2\2\u0123\36")
        buf.write("\3\2\2\2\u0124\u0125\7@\2\2\u0125\u0126\7@\2\2\u0126 ")
        buf.write("\3\2\2\2\u0127\u0128\7?\2\2\u0128\u0129\7?\2\2\u0129\"")
        buf.write("\3\2\2\2\u012a\u012b\7#\2\2\u012b\u012c\7?\2\2\u012c$")
        buf.write("\3\2\2\2\u012d\u012e\7>\2\2\u012e&\3\2\2\2\u012f\u0130")
        buf.write("\7>\2\2\u0130\u0131\7?\2\2\u0131(\3\2\2\2\u0132\u0133")
        buf.write("\7@\2\2\u0133*\3\2\2\2\u0134\u0135\7@\2\2\u0135\u0136")
        buf.write("\7?\2\2\u0136,\3\2\2\2\u0137\u0138\7\u0080\2\2\u0138.")
        buf.write("\3\2\2\2\u0139\u013a\7A\2\2\u013a\60\3\2\2\2\u013b\u013c")
        buf.write("\7#\2\2\u013c\62\3\2\2\2\u013d\u013e\7c\2\2\u013e\u013f")
        buf.write("\7d\2\2\u013f\u0140\7u\2\2\u0140\64\3\2\2\2\u0141\u0142")
        buf.write("\7c\2\2\u0142\u0143\7v\2\2\u0143\u0144\7N\2\2\u0144\u0145")
        buf.write("\7c\2\2\u0145\u0146\7d\2\2\u0146\u0147\7g\2\2\u0147\u0148")
        buf.write("\7n\2\2\u0148\66\3\2\2\2\u0149\u014a\7e\2\2\u014a\u014b")
        buf.write("\7q\2\2\u014b\u014c\7w\2\2\u014c\u014d\7p\2\2\u014d\u014e")
        buf.write("\7v\2\2\u014e\u014f\7N\2\2\u014f\u0150\7c\2\2\u0150\u0151")
        buf.write("\7d\2\2\u0151\u0152\7g\2\2\u0152\u0153\7n\2\2\u01538\3")
        buf.write("\2\2\2\u0154\u0155\7i\2\2\u0155\u0156\7g\2\2\u0156\u0157")
        buf.write("\7v\2\2\u0157\u0158\7a\2\2\u0158\u0159\7e\2\2\u0159\u015a")
        buf.write("\7q\2\2\u015a\u015b\7p\2\2\u015b\u015c\7v\2\2\u015c\u015d")
        buf.write("\7g\2\2\u015d\u015e\7z\2\2\u015e\u015f\7v\2\2\u015f:\3")
        buf.write("\2\2\2\u0160\u0161\7e\2\2\u0161\u0162\7q\2\2\u0162\u0163")
        buf.write("\7p\2\2\u0163\u0164\7v\2\2\u0164\u0165\7g\2\2\u0165\u0166")
        buf.write("\7z\2\2\u0166\u0167\7v\2\2\u0167\u0168\7u\2\2\u0168<\3")
        buf.write("\2\2\2\u0169\u016a\7o\2\2\u016a\u016b\7k\2\2\u016b\u016c")
        buf.write("\7p\2\2\u016c>\3\2\2\2\u016d\u016e\7o\2\2\u016e\u016f")
        buf.write("\7c\2\2\u016f\u0170\7z\2\2\u0170@\3\2\2\2\u0171\u0172")
        buf.write("\7n\2\2\u0172\u0173\7g\2\2\u0173\u0174\7p\2\2\u0174B\3")
        buf.write("\2\2\2\u0175\u0176\7v\2\2\u0176\u0177\7{\2\2\u0177\u0178")
        buf.write("\7r\2\2\u0178\u0179\7g\2\2\u0179D\3\2\2\2\u017a\u017b")
        buf.write("\7u\2\2\u017b\u017c\7v\2\2\u017c\u017d\7t\2\2\u017dF\3")
        buf.write("\2\2\2\u017e\u017f\7c\2\2\u017f\u0180\7p\2\2\u0180\u0181")
        buf.write("\7{\2\2\u0181H\3\2\2\2\u0182\u0183\7c\2\2\u0183\u0184")
        buf.write("\7n\2\2\u0184\u0185\7n\2\2\u0185J\3\2\2\2\u0186\u0187")
        buf.write("\7m\2\2\u0187\u0188\7g\2\2\u0188\u0189\7{\2\2\u0189\u018a")
        buf.write("\7u\2\2\u018aL\3\2\2\2\u018b\u018c\7j\2\2\u018c\u018d")
        buf.write("\7c\2\2\u018d\u018e\7u\2\2\u018e\u018f\7j\2\2\u018fN\3")
        buf.write("\2\2\2\u0190\u0191\7e\2\2\u0191\u0192\7j\2\2\u0192\u0193")
        buf.write("\7q\2\2\u0193\u0194\7q\2\2\u0194\u0195\7u\2\2\u0195\u0196")
        buf.write("\7g\2\2\u0196P\3\2\2\2\u0197\u0198\7g\2\2\u0198\u0199")
        buf.write("\7p\2\2\u0199\u019a\7f\2\2\u019aR\3\2\2\2\u019b\u019c")
        buf.write("\7c\2\2\u019c\u019d\7p\2\2\u019d\u019e\7f\2\2\u019e\u019f")
        buf.write("\7?\2\2\u019fT\3\2\2\2\u01a0\u01a1\7q\2\2\u01a1\u01a2")
        buf.write("\7t\2\2\u01a2\u01a3\7?\2\2\u01a3V\3\2\2\2\u01a4\u01a5")
        buf.write("\7?\2\2\u01a5\u01a6\7@\2\2\u01a6\u01a7\7?\2\2\u01a7X\3")
        buf.write("\2\2\2\u01a8\u01a9\7(\2\2\u01a9\u01aa\7?\2\2\u01aaZ\3")
        buf.write("\2\2\2\u01ab\u01ac\7~\2\2\u01ac\u01ad\7?\2\2\u01ad\\\3")
        buf.write("\2\2\2\u01ae\u01af\7`\2\2\u01af\u01b0\7?\2\2\u01b0^\3")
        buf.write("\2\2\2\u01b1\u01b2\7/\2\2\u01b2\u01b3\7?\2\2\u01b3`\3")
        buf.write("\2\2\2\u01b4\u01b5\7-\2\2\u01b5\u01b6\7?\2\2\u01b6b\3")
        buf.write("\2\2\2\u01b7\u01b8\7,\2\2\u01b8\u01b9\7?\2\2\u01b9d\3")
        buf.write("\2\2\2\u01ba\u01bb\7\61\2\2\u01bb\u01bc\7?\2\2\u01bcf")
        buf.write("\3\2\2\2\u01bd\u01be\7\61\2\2\u01be\u01bf\7\61\2\2\u01bf")
        buf.write("\u01c0\7?\2\2\u01c0h\3\2\2\2\u01c1\u01c2\7\'\2\2\u01c2")
        buf.write("\u01c3\7?\2\2\u01c3j\3\2\2\2\u01c4\u01c5\7o\2\2\u01c5")
        buf.write("\u01c6\7q\2\2\u01c6\u01c7\7f\2\2\u01c7\u01c8\7?\2\2\u01c8")
        buf.write("l\3\2\2\2\u01c9\u01ca\7,\2\2\u01ca\u01cb\7,\2\2\u01cb")
        buf.write("\u01cc\7?\2\2\u01ccn\3\2\2\2\u01cd\u01ce\7@\2\2\u01ce")
        buf.write("\u01cf\7@\2\2\u01cf\u01d0\7?\2\2\u01d0p\3\2\2\2\u01d1")
        buf.write("\u01d2\7>\2\2\u01d2\u01d3\7>\2\2\u01d3\u01d4\7?\2\2\u01d4")
        buf.write("r\3\2\2\2\u01d5\u01d7\7\17\2\2\u01d6\u01d5\3\2\2\2\u01d6")
        buf.write("\u01d7\3\2\2\2\u01d7\u01d8\3\2\2\2\u01d8\u01e5\7\f\2\2")
        buf.write("\u01d9\u01db\7\"\2\2\u01da\u01d9\3\2\2\2\u01db\u01de\3")
        buf.write("\2\2\2\u01dc\u01da\3\2\2\2\u01dc\u01dd\3\2\2\2\u01dd\u01e6")
        buf.write("\3\2\2\2\u01de\u01dc\3\2\2\2\u01df\u01e1\7\13\2\2\u01e0")
        buf.write("\u01df\3\2\2\2\u01e1\u01e4\3\2\2\2\u01e2\u01e0\3\2\2\2")
        buf.write("\u01e2\u01e3\3\2\2\2\u01e3\u01e6\3\2\2\2\u01e4\u01e2\3")
        buf.write("\2\2\2\u01e5\u01dc\3\2\2\2\u01e5\u01e2\3\2\2\2\u01e6\u01e7")
        buf.write("\3\2\2\2\u01e7\u01e8\b:\2\2\u01e8t\3\2\2\2\u01e9\u01eb")
        buf.write("\7\"\2\2\u01ea\u01e9\3\2\2\2\u01eb\u01ec\3\2\2\2\u01ec")
        buf.write("\u01ea\3\2\2\2\u01ec\u01ed\3\2\2\2\u01ed\u01f7\3\2\2\2")
        buf.write("\u01ee\u01f0\7\13\2\2\u01ef\u01ee\3\2\2\2\u01f0\u01f1")
        buf.write("\3\2\2\2\u01f1\u01ef\3\2\2\2\u01f1\u01f2\3\2\2\2\u01f2")
        buf.write("\u01f7\3\2\2\2\u01f3\u01f4\7^\2\2\u01f4\u01f7\5s:\2\u01f5")
        buf.write("\u01f7\5w<\2\u01f6\u01ea\3\2\2\2\u01f6\u01ef\3\2\2\2\u01f6")
        buf.write("\u01f3\3\2\2\2\u01f6\u01f5\3\2\2\2\u01f7\u01f8\3\2\2\2")
        buf.write("\u01f8\u01f9\b;\3\2\u01f9v\3\2\2\2\u01fa\u01fe\5{>\2\u01fb")
        buf.write("\u01fd\13\2\2\2\u01fc\u01fb\3\2\2\2\u01fd\u0200\3\2\2")
        buf.write("\2\u01fe\u01ff\3\2\2\2\u01fe\u01fc\3\2\2\2\u01ff\u0201")
        buf.write("\3\2\2\2\u0200\u01fe\3\2\2\2\u0201\u0202\5}?\2\u0202\u020b")
        buf.write("\3\2\2\2\u0203\u0207\5y=\2\u0204\u0206\n\2\2\2\u0205\u0204")
        buf.write("\3\2\2\2\u0206\u0209\3\2\2\2\u0207\u0205\3\2\2\2\u0207")
        buf.write("\u0208\3\2\2\2\u0208\u020b\3\2\2\2\u0209\u0207\3\2\2\2")
        buf.write("\u020a\u01fa\3\2\2\2\u020a\u0203\3\2\2\2\u020bx\3\2\2")
        buf.write("\2\u020c\u020d\7%\2\2\u020dz\3\2\2\2\u020e\u020f\7*\2")
        buf.write("\2\u020f\u0210\7,\2\2\u0210|\3\2\2\2\u0211\u0212\7,\2")
        buf.write("\2\u0212\u0213\7+\2\2\u0213~\3\2\2\2\u0214\u0215\7,\2")
        buf.write("\2\u0215\u0080\3\2\2\2\u0216\u0217\7c\2\2\u0217\u0218")
        buf.write("\7u\2\2\u0218\u0082\3\2\2\2\u0219\u021a\7\60\2\2\u021a")
        buf.write("\u0084\3\2\2\2\u021b\u021c\7k\2\2\u021c\u021d\7o\2\2\u021d")
        buf.write("\u021e\7r\2\2\u021e\u021f\7q\2\2\u021f\u0220\7t\2\2\u0220")
        buf.write("\u0221\7v\2\2\u0221\u0086\3\2\2\2\u0222\u0223\7r\2\2\u0223")
        buf.write("\u0224\7t\2\2\u0224\u0225\7k\2\2\u0225\u0226\7p\2\2\u0226")
        buf.write("\u0227\7v\2\2\u0227\u0088\3\2\2\2\u0228\u0229\7h\2\2\u0229")
        buf.write("\u022a\7t\2\2\u022a\u022b\7q\2\2\u022b\u022c\7o\2\2\u022c")
        buf.write("\u008a\3\2\2\2\u022d\u022e\7\60\2\2\u022e\u022f\7\60\2")
        buf.write("\2\u022f\u008c\3\2\2\2\u0230\u0231\7u\2\2\u0231\u0232")
        buf.write("\7g\2\2\u0232\u0233\7v\2\2\u0233\u0234\7k\2\2\u0234\u0235")
        buf.write("\7p\2\2\u0235\u0236\7v\2\2\u0236\u0237\7n\2\2\u0237\u0238")
        buf.write("\7g\2\2\u0238\u0239\7x\2\2\u0239\u023a\7g\2\2\u023a\u023b")
        buf.write("\7n\2\2\u023b\u008e\3\2\2\2\u023c\u023d\7/\2\2\u023d\u023e")
        buf.write("\7@\2\2\u023e\u0090\3\2\2\2\u023f\u0240\7u\2\2\u0240\u0241")
        buf.write("\7c\2\2\u0241\u0242\7x\2\2\u0242\u0243\7g\2\2\u0243\u0092")
        buf.write("\3\2\2\2\u0244\u0245\7u\2\2\u0245\u0246\7v\2\2\u0246\u0247")
        buf.write("\7q\2\2\u0247\u0248\7r\2\2\u0248\u0094\3\2\2\2\u0249\u024a")
        buf.write("\7n\2\2\u024a\u024b\7c\2\2\u024b\u024c\7o\2\2\u024c\u024d")
        buf.write("\7d\2\2\u024d\u024e\7f\2\2\u024e\u024f\7c\2\2\u024f\u0096")
        buf.write("\3\2\2\2\u0250\u0251\7p\2\2\u0251\u0252\7q\2\2\u0252\u0253")
        buf.write("\7v\2\2\u0253\u0098\3\2\2\2\u0254\u0255\7.\2\2\u0255\u009a")
        buf.write("\3\2\2\2\u0256\u0257\7e\2\2\u0257\u0258\7q\2\2\u0258\u0259")
        buf.write("\7p\2\2\u0259\u025a\7u\2\2\u025a\u025b\7v\2\2\u025b\u009c")
        buf.write("\3\2\2\2\u025c\u025d\7c\2\2\u025d\u025e\7y\2\2\u025e\u025f")
        buf.write("\7c\2\2\u025f\u0260\7k\2\2\u0260\u0261\7v\2\2\u0261\u009e")
        buf.write("\3\2\2\2\u0262\u0263\7c\2\2\u0263\u0264\7u\2\2\u0264\u0265")
        buf.write("\7u\2\2\u0265\u0266\7g\2\2\u0266\u0267\7t\2\2\u0267\u0268")
        buf.write("\7v\2\2\u0268\u00a0\3\2\2\2\u0269\u026a\7x\2\2\u026a\u026b")
        buf.write("\7c\2\2\u026b\u026c\7t\2\2\u026c\u00a2\3\2\2\2\u026d\u026e")
        buf.write("\7v\2\2\u026e\u026f\7t\2\2\u026f\u0270\7c\2\2\u0270\u0271")
        buf.write("\7r\2\2\u0271\u00a4\3\2\2\2\u0272\u0273\7r\2\2\u0273\u0274")
        buf.write("\7c\2\2\u0274\u0275\7u\2\2\u0275\u0276\7u\2\2\u0276\u00a6")
        buf.write("\3\2\2\2\u0277\u0278\7f\2\2\u0278\u0279\7g\2\2\u0279\u027a")
        buf.write("\7n\2\2\u027a\u00a8\3\2\2\2\u027b\u027c\7u\2\2\u027c\u027d")
        buf.write("\7r\2\2\u027d\u027e\7c\2\2\u027e\u027f\7y\2\2\u027f\u0280")
        buf.write("\7p\2\2\u0280\u00aa\3\2\2\2\u0281\u0282\7h\2\2\u0282\u0283")
        buf.write("\7k\2\2\u0283\u0284\7p\2\2\u0284\u0285\7c\2\2\u0285\u0286")
        buf.write("\7n\2\2\u0286\u0287\7n\2\2\u0287\u0288\7{\2\2\u0288\u00ac")
        buf.write("\3\2\2\2\u0289\u028a\7k\2\2\u028a\u028b\7p\2\2\u028b\u028c")
        buf.write("\7x\2\2\u028c\u028d\7c\2\2\u028d\u028e\7t\2\2\u028e\u028f")
        buf.write("\7k\2\2\u028f\u0290\7c\2\2\u0290\u0291\7p\2\2\u0291\u0292")
        buf.write("\7v\2\2\u0292\u00ae\3\2\2\2\u0293\u0294\7i\2\2\u0294\u0295")
        buf.write("\7q\2\2\u0295\u00b0\3\2\2\2\u0296\u0297\7d\2\2\u0297\u0298")
        buf.write("\7w\2\2\u0298\u0299\7k\2\2\u0299\u029a\7n\2\2\u029a\u029b")
        buf.write("\7v\2\2\u029b\u029c\7k\2\2\u029c\u029d\7p\2\2\u029d\u00b2")
        buf.write("\3\2\2\2\u029e\u029f\7u\2\2\u029f\u02a0\7g\2\2\u02a0\u02a1")
        buf.write("\7s\2\2\u02a1\u02a2\7w\2\2\u02a2\u02a3\7g\2\2\u02a3\u02a4")
        buf.write("\7p\2\2\u02a4\u02a5\7v\2\2\u02a5\u02a6\7k\2\2\u02a6\u02a7")
        buf.write("\7c\2\2\u02a7\u02a8\7n\2\2\u02a8\u00b4\3\2\2\2\u02a9\u02aa")
        buf.write("\7y\2\2\u02aa\u02ab\7j\2\2\u02ab\u02ac\7g\2\2\u02ac\u02ad")
        buf.write("\7p\2\2\u02ad\u00b6\3\2\2\2\u02ae\u02af\7n\2\2\u02af\u02b0")
        buf.write("\7g\2\2\u02b0\u02b1\7v\2\2\u02b1\u00b8\3\2\2\2\u02b2\u02b3")
        buf.write("\7k\2\2\u02b3\u02b4\7h\2\2\u02b4\u00ba\3\2\2\2\u02b5\u02b6")
        buf.write("\7g\2\2\u02b6\u02b7\7n\2\2\u02b7\u02b8\7k\2\2\u02b8\u02b9")
        buf.write("\7h\2\2\u02b9\u00bc\3\2\2\2\u02ba\u02bb\7g\2\2\u02bb\u02bc")
        buf.write("\7n\2\2\u02bc\u02bd\7u\2\2\u02bd\u02be\7g\2\2\u02be\u00be")
        buf.write("\3\2\2\2\u02bf\u02c0\7B\2\2\u02c0\u00c0\3\2\2\2\u02c1")
        buf.write("\u02c2\7y\2\2\u02c2\u02c3\7j\2\2\u02c3\u02c4\7k\2\2\u02c4")
        buf.write("\u02c5\7n\2\2\u02c5\u02c6\7g\2\2\u02c6\u00c2\3\2\2\2\u02c7")
        buf.write("\u02c8\7f\2\2\u02c8\u02c9\7g\2\2\u02c9\u02ca\7h\2\2\u02ca")
        buf.write("\u00c4\3\2\2\2\u02cb\u02cc\7t\2\2\u02cc\u02cd\7g\2\2\u02cd")
        buf.write("\u02ce\7v\2\2\u02ce\u02cf\7w\2\2\u02cf\u02d0\7t\2\2\u02d0")
        buf.write("\u02d1\7p\2\2\u02d1\u02d2\7u\2\2\u02d2\u00c6\3\2\2\2\u02d3")
        buf.write("\u02d4\7g\2\2\u02d4\u02d5\7z\2\2\u02d5\u02d6\7k\2\2\u02d6")
        buf.write("\u02d7\7u\2\2\u02d7\u02d8\7v\2\2\u02d8\u02d9\7u\2\2\u02d9")
        buf.write("\u00c8\3\2\2\2\u02da\u02db\7y\2\2\u02db\u02dc\7j\2\2\u02dc")
        buf.write("\u02dd\7g\2\2\u02dd\u02de\7t\2\2\u02de\u02df\7g\2\2\u02df")
        buf.write("\u00ca\3\2\2\2\u02e0\u02e1\7?\2\2\u02e1\u00cc\3\2\2\2")
        buf.write("\u02e2\u02e3\7h\2\2\u02e3\u02e4\7q\2\2\u02e4\u02e5\7t")
        buf.write("\2\2\u02e5\u02e6\3\2\2\2\u02e6\u02e7\bg\4\2\u02e7\u00ce")
        buf.write("\3\2\2\2\u02e8\u02e9\7k\2\2\u02e9\u02ea\7p\2\2\u02ea\u02eb")
        buf.write("\3\2\2\2\u02eb\u02ec\bh\5\2\u02ec\u00d0\3\2\2\2\u02ed")
        buf.write("\u02ee\7<\2\2\u02ee\u00d2\3\2\2\2\u02ef\u02f0\7P\2\2\u02f0")
        buf.write("\u02f1\7q\2\2\u02f1\u02f2\7p\2\2\u02f2\u02f3\7g\2\2\u02f3")
        buf.write("\u00d4\3\2\2\2\u02f4\u02f5\7c\2\2\u02f5\u02f6\7v\2\2\u02f6")
        buf.write("\u02f7\7q\2\2\u02f7\u02f8\7o\2\2\u02f8\u02f9\7k\2\2\u02f9")
        buf.write("\u02fa\7e\2\2\u02fa\u02fb\7c\2\2\u02fb\u02fc\7n\2\2\u02fc")
        buf.write("\u02fd\7n\2\2\u02fd\u02fe\7{\2\2\u02fe\u00d6\3\2\2\2\u02ff")
        buf.write("\u0300\7H\2\2\u0300\u0301\7c\2\2\u0301\u0302\7n\2\2\u0302")
        buf.write("\u0303\7u\2\2\u0303\u0309\7g\2\2\u0304\u0305\7V\2\2\u0305")
        buf.write("\u0306\7t\2\2\u0306\u0307\7w\2\2\u0307\u0309\7g\2\2\u0308")
        buf.write("\u02ff\3\2\2\2\u0308\u0304\3\2\2\2\u0309\u00d8\3\2\2\2")
        buf.write("\u030a\u030b\7g\2\2\u030b\u030c\7v\2\2\u030c\u030d\7g")
        buf.write("\2\2\u030d\u030e\7t\2\2\u030e\u030f\7p\2\2\u030f\u0310")
        buf.write("\7c\2\2\u0310\u0311\7n\2\2\u0311\u00da\3\2\2\2\u0312\u0314")
        buf.write("\t\3\2\2\u0313\u0312\3\2\2\2\u0314\u0315\3\2\2\2\u0315")
        buf.write("\u0313\3\2\2\2\u0315\u0316\3\2\2\2\u0316\u0330\3\2\2\2")
        buf.write("\u0317\u0318\7\62\2\2\u0318\u0319\7z\2\2\u0319\u031b\3")
        buf.write("\2\2\2\u031a\u031c\t\4\2\2\u031b\u031a\3\2\2\2\u031c\u031d")
        buf.write("\3\2\2\2\u031d\u031b\3\2\2\2\u031d\u031e\3\2\2\2\u031e")
        buf.write("\u0330\3\2\2\2\u031f\u0320\7\62\2\2\u0320\u0321\7d\2\2")
        buf.write("\u0321\u0323\3\2\2\2\u0322\u0324\t\5\2\2\u0323\u0322\3")
        buf.write("\2\2\2\u0324\u0325\3\2\2\2\u0325\u0323\3\2\2\2\u0325\u0326")
        buf.write("\3\2\2\2\u0326\u0330\3\2\2\2\u0327\u0328\7\62\2\2\u0328")
        buf.write("\u0329\7q\2\2\u0329\u032b\3\2\2\2\u032a\u032c\t\6\2\2")
        buf.write("\u032b\u032a\3\2\2\2\u032c\u032d\3\2\2\2\u032d\u032b\3")
        buf.write("\2\2\2\u032d\u032e\3\2\2\2\u032e\u0330\3\2\2\2\u032f\u0313")
        buf.write("\3\2\2\2\u032f\u0317\3\2\2\2\u032f\u031f\3\2\2\2\u032f")
        buf.write("\u0327\3\2\2\2\u0330\u00dc\3\2\2\2\u0331\u0335\t\7\2\2")
        buf.write("\u0332\u0334\t\b\2\2\u0333\u0332\3\2\2\2\u0334\u0337\3")
        buf.write("\2\2\2\u0335\u0333\3\2\2\2\u0335\u0336\3\2\2\2\u0336\u00de")
        buf.write("\3\2\2\2\u0337\u0335\3\2\2\2\u0338\u033b\t\t\2\2\u0339")
        buf.write("\u033c\5\u00e1q\2\u033a\u033c\5\u00ddo\2\u033b\u0339\3")
        buf.write("\2\2\2\u033b\u033a\3\2\2\2\u033c\u00e0\3\2\2\2\u033d\u033e")
        buf.write("\7\62\2\2\u033e\u033f\7Z\2\2\u033f\u0341\3\2\2\2\u0340")
        buf.write("\u0342\5\u00e3r\2\u0341\u0340\3\2\2\2\u0342\u0343\3\2")
        buf.write("\2\2\u0343\u0341\3\2\2\2\u0343\u0344\3\2\2\2\u0344\u00e2")
        buf.write("\3\2\2\2\u0345\u0346\t\4\2\2\u0346\u00e4\3\2\2\2\u0347")
        buf.write("\u0348\7]\2\2\u0348\u0349\bs\6\2\u0349\u00e6\3\2\2\2\u034a")
        buf.write("\u034b\7_\2\2\u034b\u034c\bt\7\2\u034c\u00e8\3\2\2\2\u034d")
        buf.write("\u034e\7}\2\2\u034e\u034f\bu\b\2\u034f\u00ea\3\2\2\2\u0350")
        buf.write("\u0351\7\177\2\2\u0351\u0352\bv\t\2\u0352\u00ec\3\2\2")
        buf.write("\2\u0353\u0354\7*\2\2\u0354\u0355\bw\n\2\u0355\u00ee\3")
        buf.write("\2\2\2\u0356\u0357\7+\2\2\u0357\u0358\bx\13\2\u0358\u00f0")
        buf.write("\3\2\2\2\u0359\u035a\7=\2\2\u035a\u00f2\3\2\2\2\u035b")
        buf.write("\u035e\5\u00f5{\2\u035c\u035e\5\u00f7|\2\u035d\u035b\3")
        buf.write("\2\2\2\u035d\u035c\3\2\2\2\u035e\u00f4\3\2\2\2\u035f\u0364")
        buf.write("\7)\2\2\u0360\u0363\5\u00fd\177\2\u0361\u0363\n\n\2\2")
        buf.write("\u0362\u0360\3\2\2\2\u0362\u0361\3\2\2\2\u0363\u0366\3")
        buf.write("\2\2\2\u0364\u0362\3\2\2\2\u0364\u0365\3\2\2\2\u0365\u0367")
        buf.write("\3\2\2\2\u0366\u0364\3\2\2\2\u0367\u0372\7)\2\2\u0368")
        buf.write("\u036d\7$\2\2\u0369\u036c\5\u00fd\177\2\u036a\u036c\n")
        buf.write("\13\2\2\u036b\u0369\3\2\2\2\u036b\u036a\3\2\2\2\u036c")
        buf.write("\u036f\3\2\2\2\u036d\u036b\3\2\2\2\u036d\u036e\3\2\2\2")
        buf.write("\u036e\u0370\3\2\2\2\u036f\u036d\3\2\2\2\u0370\u0372\7")
        buf.write("$\2\2\u0371\u035f\3\2\2\2\u0371\u0368\3\2\2\2\u0372\u00f6")
        buf.write("\3\2\2\2\u0373\u0374\7)\2\2\u0374\u0375\7)\2\2\u0375\u0376")
        buf.write("\7)\2\2\u0376\u037a\3\2\2\2\u0377\u0379\5\u00f9}\2\u0378")
        buf.write("\u0377\3\2\2\2\u0379\u037c\3\2\2\2\u037a\u037b\3\2\2\2")
        buf.write("\u037a\u0378\3\2\2\2\u037b\u037d\3\2\2\2\u037c\u037a\3")
        buf.write("\2\2\2\u037d\u037e\7)\2\2\u037e\u037f\7)\2\2\u037f\u038e")
        buf.write("\7)\2\2\u0380\u0381\7$\2\2\u0381\u0382\7$\2\2\u0382\u0383")
        buf.write("\7$\2\2\u0383\u0387\3\2\2\2\u0384\u0386\5\u00f9}\2\u0385")
        buf.write("\u0384\3\2\2\2\u0386\u0389\3\2\2\2\u0387\u0388\3\2\2\2")
        buf.write("\u0387\u0385\3\2\2\2\u0388\u038a\3\2\2\2\u0389\u0387\3")
        buf.write("\2\2\2\u038a\u038b\7$\2\2\u038b\u038c\7$\2\2\u038c\u038e")
        buf.write("\7$\2\2\u038d\u0373\3\2\2\2\u038d\u0380\3\2\2\2\u038e")
        buf.write("\u00f8\3\2\2\2\u038f\u0392\5\u00fb~\2\u0390\u0392\5\u00fd")
        buf.write("\177\2\u0391\u038f\3\2\2\2\u0391\u0390\3\2\2\2\u0392\u00fa")
        buf.write("\3\2\2\2\u0393\u0394\n\f\2\2\u0394\u00fc\3\2\2\2\u0395")
        buf.write("\u0396\7^\2\2\u0396\u039a\13\2\2\2\u0397\u0398\7^\2\2")
        buf.write("\u0398\u039a\5s:\2\u0399\u0395\3\2\2\2\u0399\u0397\3\2")
        buf.write("\2\2\u039a\u00fe\3\2\2\2!\2\u01d6\u01dc\u01e2\u01e5\u01ec")
        buf.write("\u01f1\u01f6\u01fe\u0207\u020a\u0308\u0315\u031d\u0325")
        buf.write("\u032d\u032f\u0335\u033b\u0343\u035d\u0362\u0364\u036b")
        buf.write("\u036d\u0371\u037a\u0387\u038d\u0391\u0399\f\3:\2\b\2")
        buf.write("\2\3g\3\3h\4\3s\5\3t\6\3u\7\3v\b\3w\t\3x\n")
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
    NL = 57
    WS = 58
    COMMENT_START = 59
    OPEN_MULTI_COMMENT = 60
    CLOSE_MULTI_COMMENT = 61
    STAR = 62
    AS = 63
    DOT = 64
    IMPORT = 65
    PRINT = 66
    FROM = 67
    RANGE = 68
    SETINTLEVEL = 69
    ARROW = 70
    SAVE = 71
    STOP = 72
    LAMBDA = 73
    NOT = 74
    COMMA = 75
    CONST = 76
    AWAIT = 77
    ASSERT = 78
    VAR = 79
    TRAP = 80
    PASS = 81
    DEL = 82
    SPAWN = 83
    FINALLY = 84
    INVARIANT = 85
    GO = 86
    BUILTIN = 87
    SEQUENTIAL = 88
    WHEN = 89
    LET = 90
    IF = 91
    ELIF = 92
    ELSE = 93
    AT = 94
    WHILE = 95
    DEF = 96
    RETURNS = 97
    EXISTS = 98
    WHERE = 99
    EQ = 100
    FOR = 101
    IN = 102
    COLON = 103
    NONE = 104
    ATOMICALLY = 105
    BOOL = 106
    ETERNAL = 107
    INT = 108
    NAME = 109
    ATOM = 110
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
            "'and'", "'or'", "'=>'", "'&'", "'|'", "'^'", "'-'", "'+'", 
            "'//'", "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", 
            "'!='", "'<'", "'<='", "'>'", "'>='", "'~'", "'?'", "'!'", "'abs'", 
            "'atLabel'", "'countLabel'", "'get_context'", "'contexts'", 
            "'min'", "'max'", "'len'", "'type'", "'str'", "'any'", "'all'", 
            "'keys'", "'hash'", "'choose'", "'end'", "'and='", "'or='", 
            "'=>='", "'&='", "'|='", "'^='", "'-='", "'+='", "'*='", "'/='", 
            "'//='", "'%='", "'mod='", "'**='", "'>>='", "'<<='", "'#'", 
            "'(*'", "'*)'", "'*'", "'as'", "'.'", "'import'", "'print'", 
            "'from'", "'..'", "'setintlevel'", "'->'", "'save'", "'stop'", 
            "'lambda'", "'not'", "','", "'const'", "'await'", "'assert'", 
            "'var'", "'trap'", "'pass'", "'del'", "'spawn'", "'finally'", 
            "'invariant'", "'go'", "'builtin'", "'sequential'", "'when'", 
            "'let'", "'if'", "'elif'", "'else'", "'@'", "'while'", "'def'", 
            "'returns'", "'exists'", "'where'", "'='", "'for'", "'in'", 
            "':'", "'None'", "'atomically'", "'eternal'", "'['", "']'", 
            "'{'", "'}'", "'('", "')'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "NL", "WS", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
            "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", "RANGE", "SETINTLEVEL", 
            "ARROW", "SAVE", "STOP", "LAMBDA", "NOT", "COMMA", "CONST", 
            "AWAIT", "ASSERT", "VAR", "TRAP", "PASS", "DEL", "SPAWN", "FINALLY", 
            "INVARIANT", "GO", "BUILTIN", "SEQUENTIAL", "WHEN", "LET", "IF", 
            "ELIF", "ELSE", "AT", "WHILE", "DEF", "RETURNS", "EXISTS", "WHERE", 
            "EQ", "FOR", "IN", "COLON", "NONE", "ATOMICALLY", "BOOL", "ETERNAL", 
            "INT", "NAME", "ATOM", "HEX_INTEGER", "OPEN_BRACK", "CLOSE_BRACK", 
            "OPEN_BRACES", "CLOSE_BRACES", "OPEN_PAREN", "CLOSE_PAREN", 
            "SEMI_COLON", "STRING" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "T__20", "T__21", "T__22", "T__23", "T__24", "T__25", 
                  "T__26", "T__27", "T__28", "T__29", "T__30", "T__31", 
                  "T__32", "T__33", "T__34", "T__35", "T__36", "T__37", 
                  "T__38", "T__39", "T__40", "T__41", "T__42", "T__43", 
                  "T__44", "T__45", "T__46", "T__47", "T__48", "T__49", 
                  "T__50", "T__51", "T__52", "T__53", "T__54", "T__55", 
                  "NL", "WS", "COMMENT", "COMMENT_START", "OPEN_MULTI_COMMENT", 
                  "CLOSE_MULTI_COMMENT", "STAR", "AS", "DOT", "IMPORT", 
                  "PRINT", "FROM", "RANGE", "SETINTLEVEL", "ARROW", "SAVE", 
                  "STOP", "LAMBDA", "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", 
                  "VAR", "TRAP", "PASS", "DEL", "SPAWN", "FINALLY", "INVARIANT", 
                  "GO", "BUILTIN", "SEQUENTIAL", "WHEN", "LET", "IF", "ELIF", 
                  "ELSE", "AT", "WHILE", "DEF", "RETURNS", "EXISTS", "WHERE", 
                  "EQ", "FOR", "IN", "COLON", "NONE", "ATOMICALLY", "BOOL", 
                  "ETERNAL", "INT", "NAME", "ATOM", "HEX_INTEGER", "HEX_DIGIT", 
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
            actions[56] = self.NL_action 
            actions[101] = self.FOR_action 
            actions[102] = self.IN_action 
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
     


