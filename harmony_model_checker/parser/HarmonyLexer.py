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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2{")
        buf.write("\u03b8\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("\t\u0080\4\u0081\t\u0081\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3")
        buf.write("\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\t\3\n")
        buf.write("\3\n\3\13\3\13\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3")
        buf.write("\16\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21\3\22")
        buf.write("\3\22\3\23\3\23\3\23\3\24\3\24\3\25\3\25\3\25\3\26\3\26")
        buf.write("\3\27\3\27\3\30\3\30\3\31\3\31\3\31\3\31\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\33\3\33")
        buf.write("\3\33\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\34\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3!\3!")
        buf.write("\3!\3!\3\"\3\"\3\"\3\"\3\"\3#\3#\3#\3#\3$\3$\3$\3$\3%")
        buf.write("\3%\3%\3%\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3(\3(\3(")
        buf.write("\3(\3(\3(\3(\3)\3)\3)\3)\3*\3*\3*\3*\3*\3+\3+\3+\3+\3")
        buf.write(",\3,\3,\3,\3-\3-\3-\3.\3.\3.\3/\3/\3/\3\60\3\60\3\60\3")
        buf.write("\61\3\61\3\61\3\62\3\62\3\62\3\63\3\63\3\63\3\64\3\64")
        buf.write("\3\64\3\64\3\65\3\65\3\65\3\66\3\66\3\66\3\66\3\66\3\67")
        buf.write("\3\67\3\67\3\67\38\38\38\38\39\39\39\39\3:\5:\u01e2\n")
        buf.write(":\3:\3:\7:\u01e6\n:\f:\16:\u01e9\13:\3:\7:\u01ec\n:\f")
        buf.write(":\16:\u01ef\13:\5:\u01f1\n:\3:\3:\3;\6;\u01f6\n;\r;\16")
        buf.write(";\u01f7\3;\6;\u01fb\n;\r;\16;\u01fc\3;\3;\3;\5;\u0202")
        buf.write("\n;\3;\3;\3<\3<\7<\u0208\n<\f<\16<\u020b\13<\3<\3<\3<")
        buf.write("\3<\7<\u0211\n<\f<\16<\u0214\13<\5<\u0216\n<\3=\3=\3>")
        buf.write("\3>\3>\3?\3?\3?\3@\3@\3A\3A\3A\3B\3B\3C\3C\3C\3C\3C\3")
        buf.write("C\3C\3D\3D\3D\3D\3D\3D\3E\3E\3E\3E\3E\3F\3F\3F\3G\3G\3")
        buf.write("G\3G\3G\3G\3G\3G\3G\3G\3G\3G\3H\3H\3H\3H\3H\3I\3I\3I\3")
        buf.write("I\3I\3J\3J\3J\3J\3J\3J\3J\3K\3K\3K\3K\3L\3L\3M\3M\3M\3")
        buf.write("M\3M\3M\3N\3N\3N\3N\3N\3N\3O\3O\3O\3O\3O\3O\3O\3P\3P\3")
        buf.write("P\3P\3Q\3Q\3Q\3Q\3Q\3R\3R\3R\3R\3R\3S\3S\3S\3S\3T\3T\3")
        buf.write("T\3T\3T\3T\3U\3U\3U\3U\3U\3U\3U\3U\3V\3V\3V\3V\3V\3V\3")
        buf.write("V\3V\3V\3V\3W\3W\3W\3X\3X\3X\3X\3X\3X\3X\3X\3Y\3Y\3Y\3")
        buf.write("Y\3Y\3Y\3Y\3Y\3Y\3Y\3Y\3Z\3Z\3Z\3Z\3Z\3[\3[\3[\3[\3\\")
        buf.write("\3\\\3\\\3]\3]\3]\3]\3]\3^\3^\3^\3^\3^\3_\3_\3`\3`\3`")
        buf.write("\3`\3`\3`\3a\3a\3a\3a\3a\3a\3a\3b\3b\3b\3b\3c\3c\3c\3")
        buf.write("c\3c\3c\3c\3c\3d\3d\3d\3d\3d\3d\3d\3e\3e\3e\3e\3e\3e\3")
        buf.write("f\3f\3g\3g\3g\3g\3g\3g\3h\3h\3h\3i\3i\3i\3i\3i\3j\3j\3")
        buf.write("k\3k\3k\3k\3k\3l\3l\3l\3l\3l\3l\3l\3l\3l\3l\3l\3m\3m\3")
        buf.write("m\3m\3m\3m\3m\3m\3m\5m\u031b\nm\3n\3n\3n\3n\3n\3n\3n\3")
        buf.write("n\3o\6o\u0326\no\ro\16o\u0327\3o\3o\3o\3o\6o\u032e\no")
        buf.write("\ro\16o\u032f\3o\3o\3o\3o\6o\u0336\no\ro\16o\u0337\3o")
        buf.write("\3o\3o\3o\6o\u033e\no\ro\16o\u033f\5o\u0342\no\3p\3p\7")
        buf.write("p\u0346\np\fp\16p\u0349\13p\3q\3q\3q\5q\u034e\nq\3r\3")
        buf.write("r\3r\3r\7r\u0354\nr\fr\16r\u0357\13r\3r\3r\3s\3s\3s\3")
        buf.write("s\6s\u035f\ns\rs\16s\u0360\3t\3t\3u\3u\3u\3v\3v\3v\3w")
        buf.write("\3w\3w\3x\3x\3x\3y\3y\3y\3z\3z\3z\3{\3{\3|\3|\5|\u037b")
        buf.write("\n|\3}\3}\3}\7}\u0380\n}\f}\16}\u0383\13}\3}\3}\3}\3}")
        buf.write("\7}\u0389\n}\f}\16}\u038c\13}\3}\5}\u038f\n}\3~\3~\3~")
        buf.write("\3~\3~\7~\u0396\n~\f~\16~\u0399\13~\3~\3~\3~\3~\3~\3~")
        buf.write("\3~\3~\7~\u03a3\n~\f~\16~\u03a6\13~\3~\3~\3~\5~\u03ab")
        buf.write("\n~\3\177\3\177\5\177\u03af\n\177\3\u0080\3\u0080\3\u0081")
        buf.write("\3\u0081\3\u0081\3\u0081\5\u0081\u03b7\n\u0081\5\u0209")
        buf.write("\u0397\u03a4\2\u0082\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21")
        buf.write("\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24")
        buf.write("\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67\359\36;\37")
        buf.write("= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63e\64")
        buf.write("g\65i\66k\67m8o9q:s;u<w\2y={>}?\177@\u0081A\u0083B\u0085")
        buf.write("C\u0087D\u0089E\u008bF\u008dG\u008fH\u0091I\u0093J\u0095")
        buf.write("K\u0097L\u0099M\u009bN\u009dO\u009fP\u00a1Q\u00a3R\u00a5")
        buf.write("S\u00a7T\u00a9U\u00abV\u00adW\u00afX\u00b1Y\u00b3Z\u00b5")
        buf.write("[\u00b7\\\u00b9]\u00bb^\u00bd_\u00bf`\u00c1a\u00c3b\u00c5")
        buf.write("c\u00c7d\u00c9e\u00cbf\u00cdg\u00cfh\u00d1i\u00d3j\u00d5")
        buf.write("k\u00d7l\u00d9m\u00dbn\u00ddo\u00dfp\u00e1q\u00e3r\u00e5")
        buf.write("s\u00e7\2\u00e9t\u00ebu\u00edv\u00efw\u00f1x\u00f3y\u00f5")
        buf.write("z\u00f7{\u00f9\2\u00fb\2\u00fd\2\u00ff\2\u0101\2\3\2\r")
        buf.write("\4\2\f\f\16\17\3\2\62;\5\2\62;CHch\3\2\62\63\3\2\629\5")
        buf.write("\2C\\aac|\6\2\62;C\\aac|\3\2\60\60\6\2\f\f\16\17))^^\6")
        buf.write("\2\f\f\16\17$$^^\3\2^^\2\u03d3\2\3\3\2\2\2\2\5\3\2\2\2")
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
        buf.write("\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2")
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
        buf.write("\2\2\u00e3\3\2\2\2\2\u00e5\3\2\2\2\2\u00e9\3\2\2\2\2\u00eb")
        buf.write("\3\2\2\2\2\u00ed\3\2\2\2\2\u00ef\3\2\2\2\2\u00f1\3\2\2")
        buf.write("\2\2\u00f3\3\2\2\2\2\u00f5\3\2\2\2\2\u00f7\3\2\2\2\3\u0103")
        buf.write("\3\2\2\2\5\u0107\3\2\2\2\7\u010a\3\2\2\2\t\u010c\3\2\2")
        buf.write("\2\13\u010e\3\2\2\2\r\u0110\3\2\2\2\17\u0112\3\2\2\2\21")
        buf.write("\u0114\3\2\2\2\23\u0117\3\2\2\2\25\u0119\3\2\2\2\27\u011b")
        buf.write("\3\2\2\2\31\u011f\3\2\2\2\33\u0122\3\2\2\2\35\u0125\3")
        buf.write("\2\2\2\37\u0128\3\2\2\2!\u012b\3\2\2\2#\u012e\3\2\2\2")
        buf.write("%\u0130\3\2\2\2\'\u0133\3\2\2\2)\u0135\3\2\2\2+\u0138")
        buf.write("\3\2\2\2-\u013a\3\2\2\2/\u013c\3\2\2\2\61\u013e\3\2\2")
        buf.write("\2\63\u0142\3\2\2\2\65\u014a\3\2\2\2\67\u0155\3\2\2\2")
        buf.write("9\u0161\3\2\2\2;\u016b\3\2\2\2=\u0174\3\2\2\2?\u0178\3")
        buf.write("\2\2\2A\u017c\3\2\2\2C\u0180\3\2\2\2E\u0185\3\2\2\2G\u0189")
        buf.write("\3\2\2\2I\u018d\3\2\2\2K\u0191\3\2\2\2M\u0196\3\2\2\2")
        buf.write("O\u019b\3\2\2\2Q\u01a2\3\2\2\2S\u01a6\3\2\2\2U\u01ab\3")
        buf.write("\2\2\2W\u01af\3\2\2\2Y\u01b3\3\2\2\2[\u01b6\3\2\2\2]\u01b9")
        buf.write("\3\2\2\2_\u01bc\3\2\2\2a\u01bf\3\2\2\2c\u01c2\3\2\2\2")
        buf.write("e\u01c5\3\2\2\2g\u01c8\3\2\2\2i\u01cc\3\2\2\2k\u01cf\3")
        buf.write("\2\2\2m\u01d4\3\2\2\2o\u01d8\3\2\2\2q\u01dc\3\2\2\2s\u01e1")
        buf.write("\3\2\2\2u\u0201\3\2\2\2w\u0215\3\2\2\2y\u0217\3\2\2\2")
        buf.write("{\u0219\3\2\2\2}\u021c\3\2\2\2\177\u021f\3\2\2\2\u0081")
        buf.write("\u0221\3\2\2\2\u0083\u0224\3\2\2\2\u0085\u0226\3\2\2\2")
        buf.write("\u0087\u022d\3\2\2\2\u0089\u0233\3\2\2\2\u008b\u0238\3")
        buf.write("\2\2\2\u008d\u023b\3\2\2\2\u008f\u0247\3\2\2\2\u0091\u024c")
        buf.write("\3\2\2\2\u0093\u0251\3\2\2\2\u0095\u0258\3\2\2\2\u0097")
        buf.write("\u025c\3\2\2\2\u0099\u025e\3\2\2\2\u009b\u0264\3\2\2\2")
        buf.write("\u009d\u026a\3\2\2\2\u009f\u0271\3\2\2\2\u00a1\u0275\3")
        buf.write("\2\2\2\u00a3\u027a\3\2\2\2\u00a5\u027f\3\2\2\2\u00a7\u0283")
        buf.write("\3\2\2\2\u00a9\u0289\3\2\2\2\u00ab\u0291\3\2\2\2\u00ad")
        buf.write("\u029b\3\2\2\2\u00af\u029e\3\2\2\2\u00b1\u02a6\3\2\2\2")
        buf.write("\u00b3\u02b1\3\2\2\2\u00b5\u02b6\3\2\2\2\u00b7\u02ba\3")
        buf.write("\2\2\2\u00b9\u02bd\3\2\2\2\u00bb\u02c2\3\2\2\2\u00bd\u02c7")
        buf.write("\3\2\2\2\u00bf\u02c9\3\2\2\2\u00c1\u02cf\3\2\2\2\u00c3")
        buf.write("\u02d6\3\2\2\2\u00c5\u02da\3\2\2\2\u00c7\u02e2\3\2\2\2")
        buf.write("\u00c9\u02e9\3\2\2\2\u00cb\u02ef\3\2\2\2\u00cd\u02f1\3")
        buf.write("\2\2\2\u00cf\u02f7\3\2\2\2\u00d1\u02fa\3\2\2\2\u00d3\u02ff")
        buf.write("\3\2\2\2\u00d5\u0301\3\2\2\2\u00d7\u0306\3\2\2\2\u00d9")
        buf.write("\u031a\3\2\2\2\u00db\u031c\3\2\2\2\u00dd\u0341\3\2\2\2")
        buf.write("\u00df\u0343\3\2\2\2\u00e1\u034a\3\2\2\2\u00e3\u034f\3")
        buf.write("\2\2\2\u00e5\u035a\3\2\2\2\u00e7\u0362\3\2\2\2\u00e9\u0364")
        buf.write("\3\2\2\2\u00eb\u0367\3\2\2\2\u00ed\u036a\3\2\2\2\u00ef")
        buf.write("\u036d\3\2\2\2\u00f1\u0370\3\2\2\2\u00f3\u0373\3\2\2\2")
        buf.write("\u00f5\u0376\3\2\2\2\u00f7\u037a\3\2\2\2\u00f9\u038e\3")
        buf.write("\2\2\2\u00fb\u03aa\3\2\2\2\u00fd\u03ae\3\2\2\2\u00ff\u03b0")
        buf.write("\3\2\2\2\u0101\u03b6\3\2\2\2\u0103\u0104\7c\2\2\u0104")
        buf.write("\u0105\7p\2\2\u0105\u0106\7f\2\2\u0106\4\3\2\2\2\u0107")
        buf.write("\u0108\7q\2\2\u0108\u0109\7t\2\2\u0109\6\3\2\2\2\u010a")
        buf.write("\u010b\7(\2\2\u010b\b\3\2\2\2\u010c\u010d\7~\2\2\u010d")
        buf.write("\n\3\2\2\2\u010e\u010f\7`\2\2\u010f\f\3\2\2\2\u0110\u0111")
        buf.write("\7/\2\2\u0111\16\3\2\2\2\u0112\u0113\7-\2\2\u0113\20\3")
        buf.write("\2\2\2\u0114\u0115\7\61\2\2\u0115\u0116\7\61\2\2\u0116")
        buf.write("\22\3\2\2\2\u0117\u0118\7\61\2\2\u0118\24\3\2\2\2\u0119")
        buf.write("\u011a\7\'\2\2\u011a\26\3\2\2\2\u011b\u011c\7o\2\2\u011c")
        buf.write("\u011d\7q\2\2\u011d\u011e\7f\2\2\u011e\30\3\2\2\2\u011f")
        buf.write("\u0120\7,\2\2\u0120\u0121\7,\2\2\u0121\32\3\2\2\2\u0122")
        buf.write("\u0123\7>\2\2\u0123\u0124\7>\2\2\u0124\34\3\2\2\2\u0125")
        buf.write("\u0126\7@\2\2\u0126\u0127\7@\2\2\u0127\36\3\2\2\2\u0128")
        buf.write("\u0129\7?\2\2\u0129\u012a\7?\2\2\u012a \3\2\2\2\u012b")
        buf.write("\u012c\7#\2\2\u012c\u012d\7?\2\2\u012d\"\3\2\2\2\u012e")
        buf.write("\u012f\7>\2\2\u012f$\3\2\2\2\u0130\u0131\7>\2\2\u0131")
        buf.write("\u0132\7?\2\2\u0132&\3\2\2\2\u0133\u0134\7@\2\2\u0134")
        buf.write("(\3\2\2\2\u0135\u0136\7@\2\2\u0136\u0137\7?\2\2\u0137")
        buf.write("*\3\2\2\2\u0138\u0139\7\u0080\2\2\u0139,\3\2\2\2\u013a")
        buf.write("\u013b\7A\2\2\u013b.\3\2\2\2\u013c\u013d\7#\2\2\u013d")
        buf.write("\60\3\2\2\2\u013e\u013f\7c\2\2\u013f\u0140\7d\2\2\u0140")
        buf.write("\u0141\7u\2\2\u0141\62\3\2\2\2\u0142\u0143\7c\2\2\u0143")
        buf.write("\u0144\7v\2\2\u0144\u0145\7N\2\2\u0145\u0146\7c\2\2\u0146")
        buf.write("\u0147\7d\2\2\u0147\u0148\7g\2\2\u0148\u0149\7n\2\2\u0149")
        buf.write("\64\3\2\2\2\u014a\u014b\7e\2\2\u014b\u014c\7q\2\2\u014c")
        buf.write("\u014d\7w\2\2\u014d\u014e\7p\2\2\u014e\u014f\7v\2\2\u014f")
        buf.write("\u0150\7N\2\2\u0150\u0151\7c\2\2\u0151\u0152\7d\2\2\u0152")
        buf.write("\u0153\7g\2\2\u0153\u0154\7n\2\2\u0154\66\3\2\2\2\u0155")
        buf.write("\u0156\7i\2\2\u0156\u0157\7g\2\2\u0157\u0158\7v\2\2\u0158")
        buf.write("\u0159\7a\2\2\u0159\u015a\7e\2\2\u015a\u015b\7q\2\2\u015b")
        buf.write("\u015c\7p\2\2\u015c\u015d\7v\2\2\u015d\u015e\7g\2\2\u015e")
        buf.write("\u015f\7z\2\2\u015f\u0160\7v\2\2\u01608\3\2\2\2\u0161")
        buf.write("\u0162\7i\2\2\u0162\u0163\7g\2\2\u0163\u0164\7v\2\2\u0164")
        buf.write("\u0165\7a\2\2\u0165\u0166\7k\2\2\u0166\u0167\7f\2\2\u0167")
        buf.write("\u0168\7g\2\2\u0168\u0169\7p\2\2\u0169\u016a\7v\2\2\u016a")
        buf.write(":\3\2\2\2\u016b\u016c\7e\2\2\u016c\u016d\7q\2\2\u016d")
        buf.write("\u016e\7p\2\2\u016e\u016f\7v\2\2\u016f\u0170\7g\2\2\u0170")
        buf.write("\u0171\7z\2\2\u0171\u0172\7v\2\2\u0172\u0173\7u\2\2\u0173")
        buf.write("<\3\2\2\2\u0174\u0175\7o\2\2\u0175\u0176\7k\2\2\u0176")
        buf.write("\u0177\7p\2\2\u0177>\3\2\2\2\u0178\u0179\7o\2\2\u0179")
        buf.write("\u017a\7c\2\2\u017a\u017b\7z\2\2\u017b@\3\2\2\2\u017c")
        buf.write("\u017d\7n\2\2\u017d\u017e\7g\2\2\u017e\u017f\7p\2\2\u017f")
        buf.write("B\3\2\2\2\u0180\u0181\7v\2\2\u0181\u0182\7{\2\2\u0182")
        buf.write("\u0183\7r\2\2\u0183\u0184\7g\2\2\u0184D\3\2\2\2\u0185")
        buf.write("\u0186\7u\2\2\u0186\u0187\7v\2\2\u0187\u0188\7t\2\2\u0188")
        buf.write("F\3\2\2\2\u0189\u018a\7c\2\2\u018a\u018b\7p\2\2\u018b")
        buf.write("\u018c\7{\2\2\u018cH\3\2\2\2\u018d\u018e\7c\2\2\u018e")
        buf.write("\u018f\7n\2\2\u018f\u0190\7n\2\2\u0190J\3\2\2\2\u0191")
        buf.write("\u0192\7m\2\2\u0192\u0193\7g\2\2\u0193\u0194\7{\2\2\u0194")
        buf.write("\u0195\7u\2\2\u0195L\3\2\2\2\u0196\u0197\7j\2\2\u0197")
        buf.write("\u0198\7c\2\2\u0198\u0199\7u\2\2\u0199\u019a\7j\2\2\u019a")
        buf.write("N\3\2\2\2\u019b\u019c\7e\2\2\u019c\u019d\7j\2\2\u019d")
        buf.write("\u019e\7q\2\2\u019e\u019f\7q\2\2\u019f\u01a0\7u\2\2\u01a0")
        buf.write("\u01a1\7g\2\2\u01a1P\3\2\2\2\u01a2\u01a3\7g\2\2\u01a3")
        buf.write("\u01a4\7p\2\2\u01a4\u01a5\7f\2\2\u01a5R\3\2\2\2\u01a6")
        buf.write("\u01a7\7c\2\2\u01a7\u01a8\7p\2\2\u01a8\u01a9\7f\2\2\u01a9")
        buf.write("\u01aa\7?\2\2\u01aaT\3\2\2\2\u01ab\u01ac\7q\2\2\u01ac")
        buf.write("\u01ad\7t\2\2\u01ad\u01ae\7?\2\2\u01aeV\3\2\2\2\u01af")
        buf.write("\u01b0\7?\2\2\u01b0\u01b1\7@\2\2\u01b1\u01b2\7?\2\2\u01b2")
        buf.write("X\3\2\2\2\u01b3\u01b4\7(\2\2\u01b4\u01b5\7?\2\2\u01b5")
        buf.write("Z\3\2\2\2\u01b6\u01b7\7~\2\2\u01b7\u01b8\7?\2\2\u01b8")
        buf.write("\\\3\2\2\2\u01b9\u01ba\7`\2\2\u01ba\u01bb\7?\2\2\u01bb")
        buf.write("^\3\2\2\2\u01bc\u01bd\7/\2\2\u01bd\u01be\7?\2\2\u01be")
        buf.write("`\3\2\2\2\u01bf\u01c0\7-\2\2\u01c0\u01c1\7?\2\2\u01c1")
        buf.write("b\3\2\2\2\u01c2\u01c3\7,\2\2\u01c3\u01c4\7?\2\2\u01c4")
        buf.write("d\3\2\2\2\u01c5\u01c6\7\61\2\2\u01c6\u01c7\7?\2\2\u01c7")
        buf.write("f\3\2\2\2\u01c8\u01c9\7\61\2\2\u01c9\u01ca\7\61\2\2\u01ca")
        buf.write("\u01cb\7?\2\2\u01cbh\3\2\2\2\u01cc\u01cd\7\'\2\2\u01cd")
        buf.write("\u01ce\7?\2\2\u01cej\3\2\2\2\u01cf\u01d0\7o\2\2\u01d0")
        buf.write("\u01d1\7q\2\2\u01d1\u01d2\7f\2\2\u01d2\u01d3\7?\2\2\u01d3")
        buf.write("l\3\2\2\2\u01d4\u01d5\7,\2\2\u01d5\u01d6\7,\2\2\u01d6")
        buf.write("\u01d7\7?\2\2\u01d7n\3\2\2\2\u01d8\u01d9\7@\2\2\u01d9")
        buf.write("\u01da\7@\2\2\u01da\u01db\7?\2\2\u01dbp\3\2\2\2\u01dc")
        buf.write("\u01dd\7>\2\2\u01dd\u01de\7>\2\2\u01de\u01df\7?\2\2\u01df")
        buf.write("r\3\2\2\2\u01e0\u01e2\7\17\2\2\u01e1\u01e0\3\2\2\2\u01e1")
        buf.write("\u01e2\3\2\2\2\u01e2\u01e3\3\2\2\2\u01e3\u01f0\7\f\2\2")
        buf.write("\u01e4\u01e6\7\"\2\2\u01e5\u01e4\3\2\2\2\u01e6\u01e9\3")
        buf.write("\2\2\2\u01e7\u01e5\3\2\2\2\u01e7\u01e8\3\2\2\2\u01e8\u01f1")
        buf.write("\3\2\2\2\u01e9\u01e7\3\2\2\2\u01ea\u01ec\7\13\2\2\u01eb")
        buf.write("\u01ea\3\2\2\2\u01ec\u01ef\3\2\2\2\u01ed\u01eb\3\2\2\2")
        buf.write("\u01ed\u01ee\3\2\2\2\u01ee\u01f1\3\2\2\2\u01ef\u01ed\3")
        buf.write("\2\2\2\u01f0\u01e7\3\2\2\2\u01f0\u01ed\3\2\2\2\u01f1\u01f2")
        buf.write("\3\2\2\2\u01f2\u01f3\b:\2\2\u01f3t\3\2\2\2\u01f4\u01f6")
        buf.write("\7\"\2\2\u01f5\u01f4\3\2\2\2\u01f6\u01f7\3\2\2\2\u01f7")
        buf.write("\u01f5\3\2\2\2\u01f7\u01f8\3\2\2\2\u01f8\u0202\3\2\2\2")
        buf.write("\u01f9\u01fb\7\13\2\2\u01fa\u01f9\3\2\2\2\u01fb\u01fc")
        buf.write("\3\2\2\2\u01fc\u01fa\3\2\2\2\u01fc\u01fd\3\2\2\2\u01fd")
        buf.write("\u0202\3\2\2\2\u01fe\u01ff\7^\2\2\u01ff\u0202\5s:\2\u0200")
        buf.write("\u0202\5w<\2\u0201\u01f5\3\2\2\2\u0201\u01fa\3\2\2\2\u0201")
        buf.write("\u01fe\3\2\2\2\u0201\u0200\3\2\2\2\u0202\u0203\3\2\2\2")
        buf.write("\u0203\u0204\b;\3\2\u0204v\3\2\2\2\u0205\u0209\5{>\2\u0206")
        buf.write("\u0208\13\2\2\2\u0207\u0206\3\2\2\2\u0208\u020b\3\2\2")
        buf.write("\2\u0209\u020a\3\2\2\2\u0209\u0207\3\2\2\2\u020a\u020c")
        buf.write("\3\2\2\2\u020b\u0209\3\2\2\2\u020c\u020d\5}?\2\u020d\u0216")
        buf.write("\3\2\2\2\u020e\u0212\5y=\2\u020f\u0211\n\2\2\2\u0210\u020f")
        buf.write("\3\2\2\2\u0211\u0214\3\2\2\2\u0212\u0210\3\2\2\2\u0212")
        buf.write("\u0213\3\2\2\2\u0213\u0216\3\2\2\2\u0214\u0212\3\2\2\2")
        buf.write("\u0215\u0205\3\2\2\2\u0215\u020e\3\2\2\2\u0216x\3\2\2")
        buf.write("\2\u0217\u0218\7%\2\2\u0218z\3\2\2\2\u0219\u021a\7*\2")
        buf.write("\2\u021a\u021b\7,\2\2\u021b|\3\2\2\2\u021c\u021d\7,\2")
        buf.write("\2\u021d\u021e\7+\2\2\u021e~\3\2\2\2\u021f\u0220\7,\2")
        buf.write("\2\u0220\u0080\3\2\2\2\u0221\u0222\7c\2\2\u0222\u0223")
        buf.write("\7u\2\2\u0223\u0082\3\2\2\2\u0224\u0225\7\60\2\2\u0225")
        buf.write("\u0084\3\2\2\2\u0226\u0227\7k\2\2\u0227\u0228\7o\2\2\u0228")
        buf.write("\u0229\7r\2\2\u0229\u022a\7q\2\2\u022a\u022b\7t\2\2\u022b")
        buf.write("\u022c\7v\2\2\u022c\u0086\3\2\2\2\u022d\u022e\7r\2\2\u022e")
        buf.write("\u022f\7t\2\2\u022f\u0230\7k\2\2\u0230\u0231\7p\2\2\u0231")
        buf.write("\u0232\7v\2\2\u0232\u0088\3\2\2\2\u0233\u0234\7h\2\2\u0234")
        buf.write("\u0235\7t\2\2\u0235\u0236\7q\2\2\u0236\u0237\7o\2\2\u0237")
        buf.write("\u008a\3\2\2\2\u0238\u0239\7\60\2\2\u0239\u023a\7\60\2")
        buf.write("\2\u023a\u008c\3\2\2\2\u023b\u023c\7u\2\2\u023c\u023d")
        buf.write("\7g\2\2\u023d\u023e\7v\2\2\u023e\u023f\7k\2\2\u023f\u0240")
        buf.write("\7p\2\2\u0240\u0241\7v\2\2\u0241\u0242\7n\2\2\u0242\u0243")
        buf.write("\7g\2\2\u0243\u0244\7x\2\2\u0244\u0245\7g\2\2\u0245\u0246")
        buf.write("\7n\2\2\u0246\u008e\3\2\2\2\u0247\u0248\7u\2\2\u0248\u0249")
        buf.write("\7c\2\2\u0249\u024a\7x\2\2\u024a\u024b\7g\2\2\u024b\u0090")
        buf.write("\3\2\2\2\u024c\u024d\7u\2\2\u024d\u024e\7v\2\2\u024e\u024f")
        buf.write("\7q\2\2\u024f\u0250\7r\2\2\u0250\u0092\3\2\2\2\u0251\u0252")
        buf.write("\7n\2\2\u0252\u0253\7c\2\2\u0253\u0254\7o\2\2\u0254\u0255")
        buf.write("\7d\2\2\u0255\u0256\7f\2\2\u0256\u0257\7c\2\2\u0257\u0094")
        buf.write("\3\2\2\2\u0258\u0259\7p\2\2\u0259\u025a\7q\2\2\u025a\u025b")
        buf.write("\7v\2\2\u025b\u0096\3\2\2\2\u025c\u025d\7.\2\2\u025d\u0098")
        buf.write("\3\2\2\2\u025e\u025f\7e\2\2\u025f\u0260\7q\2\2\u0260\u0261")
        buf.write("\7p\2\2\u0261\u0262\7u\2\2\u0262\u0263\7v\2\2\u0263\u009a")
        buf.write("\3\2\2\2\u0264\u0265\7c\2\2\u0265\u0266\7y\2\2\u0266\u0267")
        buf.write("\7c\2\2\u0267\u0268\7k\2\2\u0268\u0269\7v\2\2\u0269\u009c")
        buf.write("\3\2\2\2\u026a\u026b\7c\2\2\u026b\u026c\7u\2\2\u026c\u026d")
        buf.write("\7u\2\2\u026d\u026e\7g\2\2\u026e\u026f\7t\2\2\u026f\u0270")
        buf.write("\7v\2\2\u0270\u009e\3\2\2\2\u0271\u0272\7x\2\2\u0272\u0273")
        buf.write("\7c\2\2\u0273\u0274\7t\2\2\u0274\u00a0\3\2\2\2\u0275\u0276")
        buf.write("\7v\2\2\u0276\u0277\7t\2\2\u0277\u0278\7c\2\2\u0278\u0279")
        buf.write("\7r\2\2\u0279\u00a2\3\2\2\2\u027a\u027b\7r\2\2\u027b\u027c")
        buf.write("\7c\2\2\u027c\u027d\7u\2\2\u027d\u027e\7u\2\2\u027e\u00a4")
        buf.write("\3\2\2\2\u027f\u0280\7f\2\2\u0280\u0281\7g\2\2\u0281\u0282")
        buf.write("\7n\2\2\u0282\u00a6\3\2\2\2\u0283\u0284\7u\2\2\u0284\u0285")
        buf.write("\7r\2\2\u0285\u0286\7c\2\2\u0286\u0287\7y\2\2\u0287\u0288")
        buf.write("\7p\2\2\u0288\u00a8\3\2\2\2\u0289\u028a\7h\2\2\u028a\u028b")
        buf.write("\7k\2\2\u028b\u028c\7p\2\2\u028c\u028d\7c\2\2\u028d\u028e")
        buf.write("\7n\2\2\u028e\u028f\7n\2\2\u028f\u0290\7{\2\2\u0290\u00aa")
        buf.write("\3\2\2\2\u0291\u0292\7k\2\2\u0292\u0293\7p\2\2\u0293\u0294")
        buf.write("\7x\2\2\u0294\u0295\7c\2\2\u0295\u0296\7t\2\2\u0296\u0297")
        buf.write("\7k\2\2\u0297\u0298\7c\2\2\u0298\u0299\7p\2\2\u0299\u029a")
        buf.write("\7v\2\2\u029a\u00ac\3\2\2\2\u029b\u029c\7i\2\2\u029c\u029d")
        buf.write("\7q\2\2\u029d\u00ae\3\2\2\2\u029e\u029f\7d\2\2\u029f\u02a0")
        buf.write("\7w\2\2\u02a0\u02a1\7k\2\2\u02a1\u02a2\7n\2\2\u02a2\u02a3")
        buf.write("\7v\2\2\u02a3\u02a4\7k\2\2\u02a4\u02a5\7p\2\2\u02a5\u00b0")
        buf.write("\3\2\2\2\u02a6\u02a7\7u\2\2\u02a7\u02a8\7g\2\2\u02a8\u02a9")
        buf.write("\7s\2\2\u02a9\u02aa\7w\2\2\u02aa\u02ab\7g\2\2\u02ab\u02ac")
        buf.write("\7p\2\2\u02ac\u02ad\7v\2\2\u02ad\u02ae\7k\2\2\u02ae\u02af")
        buf.write("\7c\2\2\u02af\u02b0\7n\2\2\u02b0\u00b2\3\2\2\2\u02b1\u02b2")
        buf.write("\7y\2\2\u02b2\u02b3\7j\2\2\u02b3\u02b4\7g\2\2\u02b4\u02b5")
        buf.write("\7p\2\2\u02b5\u00b4\3\2\2\2\u02b6\u02b7\7n\2\2\u02b7\u02b8")
        buf.write("\7g\2\2\u02b8\u02b9\7v\2\2\u02b9\u00b6\3\2\2\2\u02ba\u02bb")
        buf.write("\7k\2\2\u02bb\u02bc\7h\2\2\u02bc\u00b8\3\2\2\2\u02bd\u02be")
        buf.write("\7g\2\2\u02be\u02bf\7n\2\2\u02bf\u02c0\7k\2\2\u02c0\u02c1")
        buf.write("\7h\2\2\u02c1\u00ba\3\2\2\2\u02c2\u02c3\7g\2\2\u02c3\u02c4")
        buf.write("\7n\2\2\u02c4\u02c5\7u\2\2\u02c5\u02c6\7g\2\2\u02c6\u00bc")
        buf.write("\3\2\2\2\u02c7\u02c8\7B\2\2\u02c8\u00be\3\2\2\2\u02c9")
        buf.write("\u02ca\7y\2\2\u02ca\u02cb\7j\2\2\u02cb\u02cc\7k\2\2\u02cc")
        buf.write("\u02cd\7n\2\2\u02cd\u02ce\7g\2\2\u02ce\u00c0\3\2\2\2\u02cf")
        buf.write("\u02d0\7i\2\2\u02d0\u02d1\7n\2\2\u02d1\u02d2\7q\2\2\u02d2")
        buf.write("\u02d3\7d\2\2\u02d3\u02d4\7c\2\2\u02d4\u02d5\7n\2\2\u02d5")
        buf.write("\u00c2\3\2\2\2\u02d6\u02d7\7f\2\2\u02d7\u02d8\7g\2\2\u02d8")
        buf.write("\u02d9\7h\2\2\u02d9\u00c4\3\2\2\2\u02da\u02db\7t\2\2\u02db")
        buf.write("\u02dc\7g\2\2\u02dc\u02dd\7v\2\2\u02dd\u02de\7w\2\2\u02de")
        buf.write("\u02df\7t\2\2\u02df\u02e0\7p\2\2\u02e0\u02e1\7u\2\2\u02e1")
        buf.write("\u00c6\3\2\2\2\u02e2\u02e3\7g\2\2\u02e3\u02e4\7z\2\2\u02e4")
        buf.write("\u02e5\7k\2\2\u02e5\u02e6\7u\2\2\u02e6\u02e7\7v\2\2\u02e7")
        buf.write("\u02e8\7u\2\2\u02e8\u00c8\3\2\2\2\u02e9\u02ea\7y\2\2\u02ea")
        buf.write("\u02eb\7j\2\2\u02eb\u02ec\7g\2\2\u02ec\u02ed\7t\2\2\u02ed")
        buf.write("\u02ee\7g\2\2\u02ee\u00ca\3\2\2\2\u02ef\u02f0\7?\2\2\u02f0")
        buf.write("\u00cc\3\2\2\2\u02f1\u02f2\7h\2\2\u02f2\u02f3\7q\2\2\u02f3")
        buf.write("\u02f4\7t\2\2\u02f4\u02f5\3\2\2\2\u02f5\u02f6\bg\4\2\u02f6")
        buf.write("\u00ce\3\2\2\2\u02f7\u02f8\7?\2\2\u02f8\u02f9\7@\2\2\u02f9")
        buf.write("\u00d0\3\2\2\2\u02fa\u02fb\7k\2\2\u02fb\u02fc\7p\2\2\u02fc")
        buf.write("\u02fd\3\2\2\2\u02fd\u02fe\bi\5\2\u02fe\u00d2\3\2\2\2")
        buf.write("\u02ff\u0300\7<\2\2\u0300\u00d4\3\2\2\2\u0301\u0302\7")
        buf.write("P\2\2\u0302\u0303\7q\2\2\u0303\u0304\7p\2\2\u0304\u0305")
        buf.write("\7g\2\2\u0305\u00d6\3\2\2\2\u0306\u0307\7c\2\2\u0307\u0308")
        buf.write("\7v\2\2\u0308\u0309\7q\2\2\u0309\u030a\7o\2\2\u030a\u030b")
        buf.write("\7k\2\2\u030b\u030c\7e\2\2\u030c\u030d\7c\2\2\u030d\u030e")
        buf.write("\7n\2\2\u030e\u030f\7n\2\2\u030f\u0310\7{\2\2\u0310\u00d8")
        buf.write("\3\2\2\2\u0311\u0312\7H\2\2\u0312\u0313\7c\2\2\u0313\u0314")
        buf.write("\7n\2\2\u0314\u0315\7u\2\2\u0315\u031b\7g\2\2\u0316\u0317")
        buf.write("\7V\2\2\u0317\u0318\7t\2\2\u0318\u0319\7w\2\2\u0319\u031b")
        buf.write("\7g\2\2\u031a\u0311\3\2\2\2\u031a\u0316\3\2\2\2\u031b")
        buf.write("\u00da\3\2\2\2\u031c\u031d\7g\2\2\u031d\u031e\7v\2\2\u031e")
        buf.write("\u031f\7g\2\2\u031f\u0320\7t\2\2\u0320\u0321\7p\2\2\u0321")
        buf.write("\u0322\7c\2\2\u0322\u0323\7n\2\2\u0323\u00dc\3\2\2\2\u0324")
        buf.write("\u0326\t\3\2\2\u0325\u0324\3\2\2\2\u0326\u0327\3\2\2\2")
        buf.write("\u0327\u0325\3\2\2\2\u0327\u0328\3\2\2\2\u0328\u0342\3")
        buf.write("\2\2\2\u0329\u032a\7\62\2\2\u032a\u032b\7z\2\2\u032b\u032d")
        buf.write("\3\2\2\2\u032c\u032e\t\4\2\2\u032d\u032c\3\2\2\2\u032e")
        buf.write("\u032f\3\2\2\2\u032f\u032d\3\2\2\2\u032f\u0330\3\2\2\2")
        buf.write("\u0330\u0342\3\2\2\2\u0331\u0332\7\62\2\2\u0332\u0333")
        buf.write("\7d\2\2\u0333\u0335\3\2\2\2\u0334\u0336\t\5\2\2\u0335")
        buf.write("\u0334\3\2\2\2\u0336\u0337\3\2\2\2\u0337\u0335\3\2\2\2")
        buf.write("\u0337\u0338\3\2\2\2\u0338\u0342\3\2\2\2\u0339\u033a\7")
        buf.write("\62\2\2\u033a\u033b\7q\2\2\u033b\u033d\3\2\2\2\u033c\u033e")
        buf.write("\t\6\2\2\u033d\u033c\3\2\2\2\u033e\u033f\3\2\2\2\u033f")
        buf.write("\u033d\3\2\2\2\u033f\u0340\3\2\2\2\u0340\u0342\3\2\2\2")
        buf.write("\u0341\u0325\3\2\2\2\u0341\u0329\3\2\2\2\u0341\u0331\3")
        buf.write("\2\2\2\u0341\u0339\3\2\2\2\u0342\u00de\3\2\2\2\u0343\u0347")
        buf.write("\t\7\2\2\u0344\u0346\t\b\2\2\u0345\u0344\3\2\2\2\u0346")
        buf.write("\u0349\3\2\2\2\u0347\u0345\3\2\2\2\u0347\u0348\3\2\2\2")
        buf.write("\u0348\u00e0\3\2\2\2\u0349\u0347\3\2\2\2\u034a\u034d\t")
        buf.write("\t\2\2\u034b\u034e\5\u00e5s\2\u034c\u034e\5\u00dfp\2\u034d")
        buf.write("\u034b\3\2\2\2\u034d\u034c\3\2\2\2\u034e\u00e2\3\2\2\2")
        buf.write("\u034f\u0350\7/\2\2\u0350\u0351\7@\2\2\u0351\u0355\3\2")
        buf.write("\2\2\u0352\u0354\7\"\2\2\u0353\u0352\3\2\2\2\u0354\u0357")
        buf.write("\3\2\2\2\u0355\u0353\3\2\2\2\u0355\u0356\3\2\2\2\u0356")
        buf.write("\u0358\3\2\2\2\u0357\u0355\3\2\2\2\u0358\u0359\5\u00df")
        buf.write("p\2\u0359\u00e4\3\2\2\2\u035a\u035b\7\62\2\2\u035b\u035c")
        buf.write("\7Z\2\2\u035c\u035e\3\2\2\2\u035d\u035f\5\u00e7t\2\u035e")
        buf.write("\u035d\3\2\2\2\u035f\u0360\3\2\2\2\u0360\u035e\3\2\2\2")
        buf.write("\u0360\u0361\3\2\2\2\u0361\u00e6\3\2\2\2\u0362\u0363\t")
        buf.write("\4\2\2\u0363\u00e8\3\2\2\2\u0364\u0365\7]\2\2\u0365\u0366")
        buf.write("\bu\6\2\u0366\u00ea\3\2\2\2\u0367\u0368\7_\2\2\u0368\u0369")
        buf.write("\bv\7\2\u0369\u00ec\3\2\2\2\u036a\u036b\7}\2\2\u036b\u036c")
        buf.write("\bw\b\2\u036c\u00ee\3\2\2\2\u036d\u036e\7\177\2\2\u036e")
        buf.write("\u036f\bx\t\2\u036f\u00f0\3\2\2\2\u0370\u0371\7*\2\2\u0371")
        buf.write("\u0372\by\n\2\u0372\u00f2\3\2\2\2\u0373\u0374\7+\2\2\u0374")
        buf.write("\u0375\bz\13\2\u0375\u00f4\3\2\2\2\u0376\u0377\7=\2\2")
        buf.write("\u0377\u00f6\3\2\2\2\u0378\u037b\5\u00f9}\2\u0379\u037b")
        buf.write("\5\u00fb~\2\u037a\u0378\3\2\2\2\u037a\u0379\3\2\2\2\u037b")
        buf.write("\u00f8\3\2\2\2\u037c\u0381\7)\2\2\u037d\u0380\5\u0101")
        buf.write("\u0081\2\u037e\u0380\n\n\2\2\u037f\u037d\3\2\2\2\u037f")
        buf.write("\u037e\3\2\2\2\u0380\u0383\3\2\2\2\u0381\u037f\3\2\2\2")
        buf.write("\u0381\u0382\3\2\2\2\u0382\u0384\3\2\2\2\u0383\u0381\3")
        buf.write("\2\2\2\u0384\u038f\7)\2\2\u0385\u038a\7$\2\2\u0386\u0389")
        buf.write("\5\u0101\u0081\2\u0387\u0389\n\13\2\2\u0388\u0386\3\2")
        buf.write("\2\2\u0388\u0387\3\2\2\2\u0389\u038c\3\2\2\2\u038a\u0388")
        buf.write("\3\2\2\2\u038a\u038b\3\2\2\2\u038b\u038d\3\2\2\2\u038c")
        buf.write("\u038a\3\2\2\2\u038d\u038f\7$\2\2\u038e\u037c\3\2\2\2")
        buf.write("\u038e\u0385\3\2\2\2\u038f\u00fa\3\2\2\2\u0390\u0391\7")
        buf.write(")\2\2\u0391\u0392\7)\2\2\u0392\u0393\7)\2\2\u0393\u0397")
        buf.write("\3\2\2\2\u0394\u0396\5\u00fd\177\2\u0395\u0394\3\2\2\2")
        buf.write("\u0396\u0399\3\2\2\2\u0397\u0398\3\2\2\2\u0397\u0395\3")
        buf.write("\2\2\2\u0398\u039a\3\2\2\2\u0399\u0397\3\2\2\2\u039a\u039b")
        buf.write("\7)\2\2\u039b\u039c\7)\2\2\u039c\u03ab\7)\2\2\u039d\u039e")
        buf.write("\7$\2\2\u039e\u039f\7$\2\2\u039f\u03a0\7$\2\2\u03a0\u03a4")
        buf.write("\3\2\2\2\u03a1\u03a3\5\u00fd\177\2\u03a2\u03a1\3\2\2\2")
        buf.write("\u03a3\u03a6\3\2\2\2\u03a4\u03a5\3\2\2\2\u03a4\u03a2\3")
        buf.write("\2\2\2\u03a5\u03a7\3\2\2\2\u03a6\u03a4\3\2\2\2\u03a7\u03a8")
        buf.write("\7$\2\2\u03a8\u03a9\7$\2\2\u03a9\u03ab\7$\2\2\u03aa\u0390")
        buf.write("\3\2\2\2\u03aa\u039d\3\2\2\2\u03ab\u00fc\3\2\2\2\u03ac")
        buf.write("\u03af\5\u00ff\u0080\2\u03ad\u03af\5\u0101\u0081\2\u03ae")
        buf.write("\u03ac\3\2\2\2\u03ae\u03ad\3\2\2\2\u03af\u00fe\3\2\2\2")
        buf.write("\u03b0\u03b1\n\f\2\2\u03b1\u0100\3\2\2\2\u03b2\u03b3\7")
        buf.write("^\2\2\u03b3\u03b7\13\2\2\2\u03b4\u03b5\7^\2\2\u03b5\u03b7")
        buf.write("\5s:\2\u03b6\u03b2\3\2\2\2\u03b6\u03b4\3\2\2\2\u03b7\u0102")
        buf.write("\3\2\2\2\"\2\u01e1\u01e7\u01ed\u01f0\u01f7\u01fc\u0201")
        buf.write("\u0209\u0212\u0215\u031a\u0327\u032f\u0337\u033f\u0341")
        buf.write("\u0347\u034d\u0355\u0360\u037a\u037f\u0381\u0388\u038a")
        buf.write("\u038e\u0397\u03a4\u03aa\u03ae\u03b6\f\3:\2\b\2\2\3g\3")
        buf.write("\3i\4\3u\5\3v\6\3w\7\3x\b\3y\t\3z\n")
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
    SAVE = 70
    STOP = 71
    LAMBDA = 72
    NOT = 73
    COMMA = 74
    CONST = 75
    AWAIT = 76
    ASSERT = 77
    VAR = 78
    TRAP = 79
    PASS = 80
    DEL = 81
    SPAWN = 82
    FINALLY = 83
    INVARIANT = 84
    GO = 85
    BUILTIN = 86
    SEQUENTIAL = 87
    WHEN = 88
    LET = 89
    IF = 90
    ELIF = 91
    ELSE = 92
    AT = 93
    WHILE = 94
    GLOBAL = 95
    DEF = 96
    RETURNS = 97
    EXISTS = 98
    WHERE = 99
    EQ = 100
    FOR = 101
    IMPLIES = 102
    IN = 103
    COLON = 104
    NONE = 105
    ATOMICALLY = 106
    BOOL = 107
    ETERNAL = 108
    INT = 109
    NAME = 110
    ATOM = 111
    ARROWID = 112
    HEX_INTEGER = 113
    OPEN_BRACK = 114
    CLOSE_BRACK = 115
    OPEN_BRACES = 116
    CLOSE_BRACES = 117
    OPEN_PAREN = 118
    CLOSE_PAREN = 119
    SEMI_COLON = 120
    STRING = 121

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'or'", "'&'", "'|'", "'^'", "'-'", "'+'", "'//'", 
            "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", "'!='", 
            "'<'", "'<='", "'>'", "'>='", "'~'", "'?'", "'!'", "'abs'", 
            "'atLabel'", "'countLabel'", "'get_context'", "'get_ident'", 
            "'contexts'", "'min'", "'max'", "'len'", "'type'", "'str'", 
            "'any'", "'all'", "'keys'", "'hash'", "'choose'", "'end'", "'and='", 
            "'or='", "'=>='", "'&='", "'|='", "'^='", "'-='", "'+='", "'*='", 
            "'/='", "'//='", "'%='", "'mod='", "'**='", "'>>='", "'<<='", 
            "'#'", "'(*'", "'*)'", "'*'", "'as'", "'.'", "'import'", "'print'", 
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
                  "T__50", "T__51", "T__52", "T__53", "T__54", "T__55", 
                  "NL", "WS", "COMMENT", "COMMENT_START", "OPEN_MULTI_COMMENT", 
                  "CLOSE_MULTI_COMMENT", "STAR", "AS", "DOT", "IMPORT", 
                  "PRINT", "FROM", "RANGE", "SETINTLEVEL", "SAVE", "STOP", 
                  "LAMBDA", "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", 
                  "VAR", "TRAP", "PASS", "DEL", "SPAWN", "FINALLY", "INVARIANT", 
                  "GO", "BUILTIN", "SEQUENTIAL", "WHEN", "LET", "IF", "ELIF", 
                  "ELSE", "AT", "WHILE", "GLOBAL", "DEF", "RETURNS", "EXISTS", 
                  "WHERE", "EQ", "FOR", "IMPLIES", "IN", "COLON", "NONE", 
                  "ATOMICALLY", "BOOL", "ETERNAL", "INT", "NAME", "ATOM", 
                  "ARROWID", "HEX_INTEGER", "HEX_DIGIT", "OPEN_BRACK", "CLOSE_BRACK", 
                  "OPEN_BRACES", "CLOSE_BRACES", "OPEN_PAREN", "CLOSE_PAREN", 
                  "SEMI_COLON", "STRING", "SHORT_STRING", "LONG_STRING", 
                  "LONG_STRING_ITEM", "LONG_STRING_CHAR", "STRING_ESCAPE_SEQ" ]

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
            actions[103] = self.IN_action 
            actions[115] = self.OPEN_BRACK_action 
            actions[116] = self.CLOSE_BRACK_action 
            actions[117] = self.OPEN_BRACES_action 
            actions[118] = self.CLOSE_BRACES_action 
            actions[119] = self.OPEN_PAREN_action 
            actions[120] = self.CLOSE_PAREN_action 
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
     


