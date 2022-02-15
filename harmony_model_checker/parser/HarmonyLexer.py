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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2v")
        buf.write("\u0368\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("y\ty\4z\tz\4{\t{\4|\t|\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\4")
        buf.write("\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3")
        buf.write("\n\3\n\3\13\3\13\3\f\3\f\3\r\3\r\3\r\3\r\3\16\3\16\3\16")
        buf.write("\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21\3\22\3\22")
        buf.write("\3\22\3\23\3\23\3\24\3\24\3\24\3\25\3\25\3\26\3\26\3\26")
        buf.write("\3\27\3\27\3\30\3\30\3\30\3\30\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33")
        buf.write("\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\36")
        buf.write("\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3!\3!")
        buf.write("\3!\3!\3\"\3\"\3\"\3\"\3#\3#\3#\3#\3$\3$\3$\3$\3$\3%\3")
        buf.write("%\3%\3%\3%\3&\3&\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3(\3(")
        buf.write("\3(\3(\3(\3)\3)\3)\3)\3*\3*\3*\3*\3+\3+\3+\3,\3,\3,\3")
        buf.write("-\3-\3-\3.\3.\3.\3/\3/\3/\3\60\3\60\3\60\3\61\3\61\3\61")
        buf.write("\3\62\3\62\3\62\3\62\3\63\3\63\3\63\3\64\3\64\3\64\3\64")
        buf.write("\3\64\3\65\3\65\3\65\3\65\3\66\3\66\3\66\3\66\3\67\5\67")
        buf.write("\u01cc\n\67\3\67\3\67\7\67\u01d0\n\67\f\67\16\67\u01d3")
        buf.write("\13\67\3\67\3\67\38\68\u01d8\n8\r8\168\u01d9\38\68\u01dd")
        buf.write("\n8\r8\168\u01de\38\38\38\58\u01e4\n8\38\38\39\39\79\u01ea")
        buf.write("\n9\f9\169\u01ed\139\39\39\39\39\79\u01f3\n9\f9\169\u01f6")
        buf.write("\139\59\u01f8\n9\3:\3:\3;\3;\3;\3<\3<\3<\3=\3=\3>\3>\3")
        buf.write("?\3?\3?\3@\3@\3A\3A\3A\3A\3A\3A\3A\3B\3B\3B\3B\3B\3B\3")
        buf.write("C\3C\3C\3C\3C\3D\3D\3D\3E\3E\3E\3E\3E\3E\3E\3E\3E\3E\3")
        buf.write("E\3E\3F\3F\3F\3G\3G\3G\3G\3G\3H\3H\3H\3H\3H\3I\3I\3I\3")
        buf.write("I\3I\3I\3I\3J\3J\3K\3K\3K\3K\3L\3L\3M\3M\3M\3M\3M\3M\3")
        buf.write("N\3N\3N\3N\3N\3N\3O\3O\3O\3O\3O\3O\3O\3P\3P\3P\3P\3Q\3")
        buf.write("Q\3Q\3Q\3Q\3R\3R\3R\3R\3R\3R\3R\3R\3R\3S\3S\3S\3S\3S\3")
        buf.write("T\3T\3T\3T\3U\3U\3U\3U\3U\3U\3V\3V\3V\3V\3V\3V\3V\3V\3")
        buf.write("V\3V\3W\3W\3W\3X\3X\3X\3X\3X\3X\3X\3X\3X\3X\3X\3Y\3Y\3")
        buf.write("Y\3Y\3Y\3Z\3Z\3Z\3Z\3[\3[\3[\3\\\3\\\3\\\3\\\3\\\3]\3")
        buf.write("]\3]\3]\3]\3^\3^\3_\3_\3_\3_\3_\3_\3`\3`\3`\3`\3a\3a\3")
        buf.write("a\3a\3a\3a\3a\3b\3b\3b\3b\3b\3b\3c\3c\3d\3d\3d\3d\3d\3")
        buf.write("d\3e\3e\3e\3e\3e\3f\3f\3g\3g\3g\3g\3g\3h\3h\3h\3h\3h\3")
        buf.write("h\3h\3h\3h\3h\3h\3i\3i\3i\3i\3i\3i\3i\3i\3i\5i\u02eb\n")
        buf.write("i\3j\3j\3j\3j\3j\3j\3j\3j\3k\6k\u02f6\nk\rk\16k\u02f7")
        buf.write("\3k\3k\3k\5k\u02fd\nk\3l\3l\7l\u0301\nl\fl\16l\u0304\13")
        buf.write("l\3m\3m\3m\5m\u0309\nm\3n\3n\3n\3n\6n\u030f\nn\rn\16n")
        buf.write("\u0310\3o\3o\3p\3p\3p\3q\3q\3q\3r\3r\3r\3s\3s\3s\3t\3")
        buf.write("t\3t\3u\3u\3u\3v\3v\3w\3w\5w\u032b\nw\3x\3x\3x\7x\u0330")
        buf.write("\nx\fx\16x\u0333\13x\3x\3x\3x\3x\7x\u0339\nx\fx\16x\u033c")
        buf.write("\13x\3x\5x\u033f\nx\3y\3y\3y\3y\3y\7y\u0346\ny\fy\16y")
        buf.write("\u0349\13y\3y\3y\3y\3y\3y\3y\3y\3y\7y\u0353\ny\fy\16y")
        buf.write("\u0356\13y\3y\3y\3y\5y\u035b\ny\3z\3z\5z\u035f\nz\3{\3")
        buf.write("{\3|\3|\3|\3|\5|\u0367\n|\5\u01eb\u0347\u0354\2}\3\3\5")
        buf.write("\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33")
        buf.write("\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32")
        buf.write("\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U")
        buf.write(",W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q\2s:u;w<y")
        buf.write("={>}?\177@\u0081A\u0083B\u0085C\u0087D\u0089E\u008bF\u008d")
        buf.write("G\u008fH\u0091I\u0093J\u0095K\u0097L\u0099M\u009bN\u009d")
        buf.write("O\u009fP\u00a1Q\u00a3R\u00a5S\u00a7T\u00a9U\u00abV\u00ad")
        buf.write("W\u00afX\u00b1Y\u00b3Z\u00b5[\u00b7\\\u00b9]\u00bb^\u00bd")
        buf.write("_\u00bf`\u00c1a\u00c3b\u00c5c\u00c7d\u00c9e\u00cbf\u00cd")
        buf.write("g\u00cfh\u00d1i\u00d3j\u00d5k\u00d7l\u00d9m\u00dbn\u00dd")
        buf.write("\2\u00dfo\u00e1p\u00e3q\u00e5r\u00e7s\u00e9t\u00ebu\u00ed")
        buf.write("v\u00ef\2\u00f1\2\u00f3\2\u00f5\2\u00f7\2\3\2\f\4\2\13")
        buf.write("\13\"\"\4\2\f\f\16\17\3\2\62;\5\2C\\aac|\6\2\62;C\\aa")
        buf.write("c|\3\2\60\60\5\2\62;CHch\6\2\f\f\16\17))^^\6\2\f\f\16")
        buf.write("\17$$^^\3\2^^\2\u037b\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2")
        buf.write("\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2")
        buf.write("\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2")
        buf.write("\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!")
        buf.write("\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2")
        buf.write("\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3")
        buf.write("\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2")
        buf.write("\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2")
        buf.write("\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2")
        buf.write("\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3")
        buf.write("\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c")
        buf.write("\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2")
        buf.write("m\3\2\2\2\2o\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2")
        buf.write("\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081")
        buf.write("\3\2\2\2\2\u0083\3\2\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2")
        buf.write("\2\2\u0089\3\2\2\2\2\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f")
        buf.write("\3\2\2\2\2\u0091\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2")
        buf.write("\2\2\u0097\3\2\2\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d")
        buf.write("\3\2\2\2\2\u009f\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2")
        buf.write("\2\2\u00a5\3\2\2\2\2\u00a7\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab")
        buf.write("\3\2\2\2\2\u00ad\3\2\2\2\2\u00af\3\2\2\2\2\u00b1\3\2\2")
        buf.write("\2\2\u00b3\3\2\2\2\2\u00b5\3\2\2\2\2\u00b7\3\2\2\2\2\u00b9")
        buf.write("\3\2\2\2\2\u00bb\3\2\2\2\2\u00bd\3\2\2\2\2\u00bf\3\2\2")
        buf.write("\2\2\u00c1\3\2\2\2\2\u00c3\3\2\2\2\2\u00c5\3\2\2\2\2\u00c7")
        buf.write("\3\2\2\2\2\u00c9\3\2\2\2\2\u00cb\3\2\2\2\2\u00cd\3\2\2")
        buf.write("\2\2\u00cf\3\2\2\2\2\u00d1\3\2\2\2\2\u00d3\3\2\2\2\2\u00d5")
        buf.write("\3\2\2\2\2\u00d7\3\2\2\2\2\u00d9\3\2\2\2\2\u00db\3\2\2")
        buf.write("\2\2\u00df\3\2\2\2\2\u00e1\3\2\2\2\2\u00e3\3\2\2\2\2\u00e5")
        buf.write("\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9\3\2\2\2\2\u00eb\3\2\2")
        buf.write("\2\2\u00ed\3\2\2\2\3\u00f9\3\2\2\2\5\u00fd\3\2\2\2\7\u0100")
        buf.write("\3\2\2\2\t\u0103\3\2\2\2\13\u0105\3\2\2\2\r\u0107\3\2")
        buf.write("\2\2\17\u0109\3\2\2\2\21\u010b\3\2\2\2\23\u010d\3\2\2")
        buf.write("\2\25\u0110\3\2\2\2\27\u0112\3\2\2\2\31\u0114\3\2\2\2")
        buf.write("\33\u0118\3\2\2\2\35\u011b\3\2\2\2\37\u011e\3\2\2\2!\u0121")
        buf.write("\3\2\2\2#\u0124\3\2\2\2%\u0127\3\2\2\2\'\u0129\3\2\2\2")
        buf.write(")\u012c\3\2\2\2+\u012e\3\2\2\2-\u0131\3\2\2\2/\u0133\3")
        buf.write("\2\2\2\61\u0137\3\2\2\2\63\u013f\3\2\2\2\65\u014a\3\2")
        buf.write("\2\2\67\u0156\3\2\2\29\u015f\3\2\2\2;\u0167\3\2\2\2=\u016b")
        buf.write("\3\2\2\2?\u016f\3\2\2\2A\u0173\3\2\2\2C\u0177\3\2\2\2")
        buf.write("E\u017b\3\2\2\2G\u017f\3\2\2\2I\u0184\3\2\2\2K\u0189\3")
        buf.write("\2\2\2M\u0190\3\2\2\2O\u0194\3\2\2\2Q\u0199\3\2\2\2S\u019d")
        buf.write("\3\2\2\2U\u01a1\3\2\2\2W\u01a4\3\2\2\2Y\u01a7\3\2\2\2")
        buf.write("[\u01aa\3\2\2\2]\u01ad\3\2\2\2_\u01b0\3\2\2\2a\u01b3\3")
        buf.write("\2\2\2c\u01b6\3\2\2\2e\u01ba\3\2\2\2g\u01bd\3\2\2\2i\u01c2")
        buf.write("\3\2\2\2k\u01c6\3\2\2\2m\u01cb\3\2\2\2o\u01e3\3\2\2\2")
        buf.write("q\u01f7\3\2\2\2s\u01f9\3\2\2\2u\u01fb\3\2\2\2w\u01fe\3")
        buf.write("\2\2\2y\u0201\3\2\2\2{\u0203\3\2\2\2}\u0205\3\2\2\2\177")
        buf.write("\u0208\3\2\2\2\u0081\u020a\3\2\2\2\u0083\u0211\3\2\2\2")
        buf.write("\u0085\u0217\3\2\2\2\u0087\u021c\3\2\2\2\u0089\u021f\3")
        buf.write("\2\2\2\u008b\u022b\3\2\2\2\u008d\u022e\3\2\2\2\u008f\u0233")
        buf.write("\3\2\2\2\u0091\u0238\3\2\2\2\u0093\u023f\3\2\2\2\u0095")
        buf.write("\u0241\3\2\2\2\u0097\u0245\3\2\2\2\u0099\u0247\3\2\2\2")
        buf.write("\u009b\u024d\3\2\2\2\u009d\u0253\3\2\2\2\u009f\u025a\3")
        buf.write("\2\2\2\u00a1\u025e\3\2\2\2\u00a3\u0263\3\2\2\2\u00a5\u026c")
        buf.write("\3\2\2\2\u00a7\u0271\3\2\2\2\u00a9\u0275\3\2\2\2\u00ab")
        buf.write("\u027b\3\2\2\2\u00ad\u0285\3\2\2\2\u00af\u0288\3\2\2\2")
        buf.write("\u00b1\u0293\3\2\2\2\u00b3\u0298\3\2\2\2\u00b5\u029c\3")
        buf.write("\2\2\2\u00b7\u029f\3\2\2\2\u00b9\u02a4\3\2\2\2\u00bb\u02a9")
        buf.write("\3\2\2\2\u00bd\u02ab\3\2\2\2\u00bf\u02b1\3\2\2\2\u00c1")
        buf.write("\u02b5\3\2\2\2\u00c3\u02bc\3\2\2\2\u00c5\u02c2\3\2\2\2")
        buf.write("\u00c7\u02c4\3\2\2\2\u00c9\u02ca\3\2\2\2\u00cb\u02cf\3")
        buf.write("\2\2\2\u00cd\u02d1\3\2\2\2\u00cf\u02d6\3\2\2\2\u00d1\u02ea")
        buf.write("\3\2\2\2\u00d3\u02ec\3\2\2\2\u00d5\u02fc\3\2\2\2\u00d7")
        buf.write("\u02fe\3\2\2\2\u00d9\u0305\3\2\2\2\u00db\u030a\3\2\2\2")
        buf.write("\u00dd\u0312\3\2\2\2\u00df\u0314\3\2\2\2\u00e1\u0317\3")
        buf.write("\2\2\2\u00e3\u031a\3\2\2\2\u00e5\u031d\3\2\2\2\u00e7\u0320")
        buf.write("\3\2\2\2\u00e9\u0323\3\2\2\2\u00eb\u0326\3\2\2\2\u00ed")
        buf.write("\u032a\3\2\2\2\u00ef\u033e\3\2\2\2\u00f1\u035a\3\2\2\2")
        buf.write("\u00f3\u035e\3\2\2\2\u00f5\u0360\3\2\2\2\u00f7\u0366\3")
        buf.write("\2\2\2\u00f9\u00fa\7c\2\2\u00fa\u00fb\7p\2\2\u00fb\u00fc")
        buf.write("\7f\2\2\u00fc\4\3\2\2\2\u00fd\u00fe\7q\2\2\u00fe\u00ff")
        buf.write("\7t\2\2\u00ff\6\3\2\2\2\u0100\u0101\7?\2\2\u0101\u0102")
        buf.write("\7@\2\2\u0102\b\3\2\2\2\u0103\u0104\7(\2\2\u0104\n\3\2")
        buf.write("\2\2\u0105\u0106\7~\2\2\u0106\f\3\2\2\2\u0107\u0108\7")
        buf.write("`\2\2\u0108\16\3\2\2\2\u0109\u010a\7/\2\2\u010a\20\3\2")
        buf.write("\2\2\u010b\u010c\7-\2\2\u010c\22\3\2\2\2\u010d\u010e\7")
        buf.write("\61\2\2\u010e\u010f\7\61\2\2\u010f\24\3\2\2\2\u0110\u0111")
        buf.write("\7\61\2\2\u0111\26\3\2\2\2\u0112\u0113\7\'\2\2\u0113\30")
        buf.write("\3\2\2\2\u0114\u0115\7o\2\2\u0115\u0116\7q\2\2\u0116\u0117")
        buf.write("\7f\2\2\u0117\32\3\2\2\2\u0118\u0119\7,\2\2\u0119\u011a")
        buf.write("\7,\2\2\u011a\34\3\2\2\2\u011b\u011c\7>\2\2\u011c\u011d")
        buf.write("\7>\2\2\u011d\36\3\2\2\2\u011e\u011f\7@\2\2\u011f\u0120")
        buf.write("\7@\2\2\u0120 \3\2\2\2\u0121\u0122\7?\2\2\u0122\u0123")
        buf.write("\7?\2\2\u0123\"\3\2\2\2\u0124\u0125\7#\2\2\u0125\u0126")
        buf.write("\7?\2\2\u0126$\3\2\2\2\u0127\u0128\7>\2\2\u0128&\3\2\2")
        buf.write("\2\u0129\u012a\7>\2\2\u012a\u012b\7?\2\2\u012b(\3\2\2")
        buf.write("\2\u012c\u012d\7@\2\2\u012d*\3\2\2\2\u012e\u012f\7@\2")
        buf.write("\2\u012f\u0130\7?\2\2\u0130,\3\2\2\2\u0131\u0132\7\u0080")
        buf.write("\2\2\u0132.\3\2\2\2\u0133\u0134\7c\2\2\u0134\u0135\7d")
        buf.write("\2\2\u0135\u0136\7u\2\2\u0136\60\3\2\2\2\u0137\u0138\7")
        buf.write("c\2\2\u0138\u0139\7v\2\2\u0139\u013a\7N\2\2\u013a\u013b")
        buf.write("\7c\2\2\u013b\u013c\7d\2\2\u013c\u013d\7g\2\2\u013d\u013e")
        buf.write("\7n\2\2\u013e\62\3\2\2\2\u013f\u0140\7e\2\2\u0140\u0141")
        buf.write("\7q\2\2\u0141\u0142\7w\2\2\u0142\u0143\7p\2\2\u0143\u0144")
        buf.write("\7v\2\2\u0144\u0145\7N\2\2\u0145\u0146\7c\2\2\u0146\u0147")
        buf.write("\7d\2\2\u0147\u0148\7g\2\2\u0148\u0149\7n\2\2\u0149\64")
        buf.write("\3\2\2\2\u014a\u014b\7i\2\2\u014b\u014c\7g\2\2\u014c\u014d")
        buf.write("\7v\2\2\u014d\u014e\7a\2\2\u014e\u014f\7e\2\2\u014f\u0150")
        buf.write("\7q\2\2\u0150\u0151\7p\2\2\u0151\u0152\7v\2\2\u0152\u0153")
        buf.write("\7g\2\2\u0153\u0154\7z\2\2\u0154\u0155\7v\2\2\u0155\66")
        buf.write("\3\2\2\2\u0156\u0157\7e\2\2\u0157\u0158\7q\2\2\u0158\u0159")
        buf.write("\7p\2\2\u0159\u015a\7v\2\2\u015a\u015b\7g\2\2\u015b\u015c")
        buf.write("\7z\2\2\u015c\u015d\7v\2\2\u015d\u015e\7u\2\2\u015e8\3")
        buf.write("\2\2\2\u015f\u0160\7k\2\2\u0160\u0161\7u\2\2\u0161\u0162")
        buf.write("\7G\2\2\u0162\u0163\7o\2\2\u0163\u0164\7r\2\2\u0164\u0165")
        buf.write("\7v\2\2\u0165\u0166\7{\2\2\u0166:\3\2\2\2\u0167\u0168")
        buf.write("\7o\2\2\u0168\u0169\7k\2\2\u0169\u016a\7p\2\2\u016a<\3")
        buf.write("\2\2\2\u016b\u016c\7o\2\2\u016c\u016d\7c\2\2\u016d\u016e")
        buf.write("\7z\2\2\u016e>\3\2\2\2\u016f\u0170\7n\2\2\u0170\u0171")
        buf.write("\7g\2\2\u0171\u0172\7p\2\2\u0172@\3\2\2\2\u0173\u0174")
        buf.write("\7u\2\2\u0174\u0175\7v\2\2\u0175\u0176\7t\2\2\u0176B\3")
        buf.write("\2\2\2\u0177\u0178\7c\2\2\u0178\u0179\7p\2\2\u0179\u017a")
        buf.write("\7{\2\2\u017aD\3\2\2\2\u017b\u017c\7c\2\2\u017c\u017d")
        buf.write("\7n\2\2\u017d\u017e\7n\2\2\u017eF\3\2\2\2\u017f\u0180")
        buf.write("\7m\2\2\u0180\u0181\7g\2\2\u0181\u0182\7{\2\2\u0182\u0183")
        buf.write("\7u\2\2\u0183H\3\2\2\2\u0184\u0185\7j\2\2\u0185\u0186")
        buf.write("\7c\2\2\u0186\u0187\7u\2\2\u0187\u0188\7j\2\2\u0188J\3")
        buf.write("\2\2\2\u0189\u018a\7e\2\2\u018a\u018b\7j\2\2\u018b\u018c")
        buf.write("\7q\2\2\u018c\u018d\7q\2\2\u018d\u018e\7u\2\2\u018e\u018f")
        buf.write("\7g\2\2\u018fL\3\2\2\2\u0190\u0191\7g\2\2\u0191\u0192")
        buf.write("\7p\2\2\u0192\u0193\7f\2\2\u0193N\3\2\2\2\u0194\u0195")
        buf.write("\7c\2\2\u0195\u0196\7p\2\2\u0196\u0197\7f\2\2\u0197\u0198")
        buf.write("\7?\2\2\u0198P\3\2\2\2\u0199\u019a\7q\2\2\u019a\u019b")
        buf.write("\7t\2\2\u019b\u019c\7?\2\2\u019cR\3\2\2\2\u019d\u019e")
        buf.write("\7?\2\2\u019e\u019f\7@\2\2\u019f\u01a0\7?\2\2\u01a0T\3")
        buf.write("\2\2\2\u01a1\u01a2\7(\2\2\u01a2\u01a3\7?\2\2\u01a3V\3")
        buf.write("\2\2\2\u01a4\u01a5\7~\2\2\u01a5\u01a6\7?\2\2\u01a6X\3")
        buf.write("\2\2\2\u01a7\u01a8\7`\2\2\u01a8\u01a9\7?\2\2\u01a9Z\3")
        buf.write("\2\2\2\u01aa\u01ab\7/\2\2\u01ab\u01ac\7?\2\2\u01ac\\\3")
        buf.write("\2\2\2\u01ad\u01ae\7-\2\2\u01ae\u01af\7?\2\2\u01af^\3")
        buf.write("\2\2\2\u01b0\u01b1\7,\2\2\u01b1\u01b2\7?\2\2\u01b2`\3")
        buf.write("\2\2\2\u01b3\u01b4\7\61\2\2\u01b4\u01b5\7?\2\2\u01b5b")
        buf.write("\3\2\2\2\u01b6\u01b7\7\61\2\2\u01b7\u01b8\7\61\2\2\u01b8")
        buf.write("\u01b9\7?\2\2\u01b9d\3\2\2\2\u01ba\u01bb\7\'\2\2\u01bb")
        buf.write("\u01bc\7?\2\2\u01bcf\3\2\2\2\u01bd\u01be\7o\2\2\u01be")
        buf.write("\u01bf\7q\2\2\u01bf\u01c0\7f\2\2\u01c0\u01c1\7?\2\2\u01c1")
        buf.write("h\3\2\2\2\u01c2\u01c3\7,\2\2\u01c3\u01c4\7,\2\2\u01c4")
        buf.write("\u01c5\7?\2\2\u01c5j\3\2\2\2\u01c6\u01c7\7@\2\2\u01c7")
        buf.write("\u01c8\7@\2\2\u01c8\u01c9\7?\2\2\u01c9l\3\2\2\2\u01ca")
        buf.write("\u01cc\7\17\2\2\u01cb\u01ca\3\2\2\2\u01cb\u01cc\3\2\2")
        buf.write("\2\u01cc\u01cd\3\2\2\2\u01cd\u01d1\7\f\2\2\u01ce\u01d0")
        buf.write("\t\2\2\2\u01cf\u01ce\3\2\2\2\u01d0\u01d3\3\2\2\2\u01d1")
        buf.write("\u01cf\3\2\2\2\u01d1\u01d2\3\2\2\2\u01d2\u01d4\3\2\2\2")
        buf.write("\u01d3\u01d1\3\2\2\2\u01d4\u01d5\b\67\2\2\u01d5n\3\2\2")
        buf.write("\2\u01d6\u01d8\7\"\2\2\u01d7\u01d6\3\2\2\2\u01d8\u01d9")
        buf.write("\3\2\2\2\u01d9\u01d7\3\2\2\2\u01d9\u01da\3\2\2\2\u01da")
        buf.write("\u01e4\3\2\2\2\u01db\u01dd\7\13\2\2\u01dc\u01db\3\2\2")
        buf.write("\2\u01dd\u01de\3\2\2\2\u01de\u01dc\3\2\2\2\u01de\u01df")
        buf.write("\3\2\2\2\u01df\u01e4\3\2\2\2\u01e0\u01e1\7^\2\2\u01e1")
        buf.write("\u01e4\5m\67\2\u01e2\u01e4\5q9\2\u01e3\u01d7\3\2\2\2\u01e3")
        buf.write("\u01dc\3\2\2\2\u01e3\u01e0\3\2\2\2\u01e3\u01e2\3\2\2\2")
        buf.write("\u01e4\u01e5\3\2\2\2\u01e5\u01e6\b8\3\2\u01e6p\3\2\2\2")
        buf.write("\u01e7\u01eb\5u;\2\u01e8\u01ea\13\2\2\2\u01e9\u01e8\3")
        buf.write("\2\2\2\u01ea\u01ed\3\2\2\2\u01eb\u01ec\3\2\2\2\u01eb\u01e9")
        buf.write("\3\2\2\2\u01ec\u01ee\3\2\2\2\u01ed\u01eb\3\2\2\2\u01ee")
        buf.write("\u01ef\5w<\2\u01ef\u01f8\3\2\2\2\u01f0\u01f4\5s:\2\u01f1")
        buf.write("\u01f3\n\3\2\2\u01f2\u01f1\3\2\2\2\u01f3\u01f6\3\2\2\2")
        buf.write("\u01f4\u01f2\3\2\2\2\u01f4\u01f5\3\2\2\2\u01f5\u01f8\3")
        buf.write("\2\2\2\u01f6\u01f4\3\2\2\2\u01f7\u01e7\3\2\2\2\u01f7\u01f0")
        buf.write("\3\2\2\2\u01f8r\3\2\2\2\u01f9\u01fa\7%\2\2\u01fat\3\2")
        buf.write("\2\2\u01fb\u01fc\7*\2\2\u01fc\u01fd\7,\2\2\u01fdv\3\2")
        buf.write("\2\2\u01fe\u01ff\7,\2\2\u01ff\u0200\7+\2\2\u0200x\3\2")
        buf.write("\2\2\u0201\u0202\7#\2\2\u0202z\3\2\2\2\u0203\u0204\7,")
        buf.write("\2\2\u0204|\3\2\2\2\u0205\u0206\7c\2\2\u0206\u0207\7u")
        buf.write("\2\2\u0207~\3\2\2\2\u0208\u0209\7\60\2\2\u0209\u0080\3")
        buf.write("\2\2\2\u020a\u020b\7k\2\2\u020b\u020c\7o\2\2\u020c\u020d")
        buf.write("\7r\2\2\u020d\u020e\7q\2\2\u020e\u020f\7t\2\2\u020f\u0210")
        buf.write("\7v\2\2\u0210\u0082\3\2\2\2\u0211\u0212\7r\2\2\u0212\u0213")
        buf.write("\7t\2\2\u0213\u0214\7k\2\2\u0214\u0215\7p\2\2\u0215\u0216")
        buf.write("\7v\2\2\u0216\u0084\3\2\2\2\u0217\u0218\7h\2\2\u0218\u0219")
        buf.write("\7t\2\2\u0219\u021a\7q\2\2\u021a\u021b\7o\2\2\u021b\u0086")
        buf.write("\3\2\2\2\u021c\u021d\7\60\2\2\u021d\u021e\7\60\2\2\u021e")
        buf.write("\u0088\3\2\2\2\u021f\u0220\7u\2\2\u0220\u0221\7g\2\2\u0221")
        buf.write("\u0222\7v\2\2\u0222\u0223\7k\2\2\u0223\u0224\7p\2\2\u0224")
        buf.write("\u0225\7v\2\2\u0225\u0226\7n\2\2\u0226\u0227\7g\2\2\u0227")
        buf.write("\u0228\7x\2\2\u0228\u0229\7g\2\2\u0229\u022a\7n\2\2\u022a")
        buf.write("\u008a\3\2\2\2\u022b\u022c\7/\2\2\u022c\u022d\7@\2\2\u022d")
        buf.write("\u008c\3\2\2\2\u022e\u022f\7u\2\2\u022f\u0230\7c\2\2\u0230")
        buf.write("\u0231\7x\2\2\u0231\u0232\7g\2\2\u0232\u008e\3\2\2\2\u0233")
        buf.write("\u0234\7u\2\2\u0234\u0235\7v\2\2\u0235\u0236\7q\2\2\u0236")
        buf.write("\u0237\7r\2\2\u0237\u0090\3\2\2\2\u0238\u0239\7n\2\2\u0239")
        buf.write("\u023a\7c\2\2\u023a\u023b\7o\2\2\u023b\u023c\7d\2\2\u023c")
        buf.write("\u023d\7f\2\2\u023d\u023e\7c\2\2\u023e\u0092\3\2\2\2\u023f")
        buf.write("\u0240\7A\2\2\u0240\u0094\3\2\2\2\u0241\u0242\7p\2\2\u0242")
        buf.write("\u0243\7q\2\2\u0243\u0244\7v\2\2\u0244\u0096\3\2\2\2\u0245")
        buf.write("\u0246\7.\2\2\u0246\u0098\3\2\2\2\u0247\u0248\7e\2\2\u0248")
        buf.write("\u0249\7q\2\2\u0249\u024a\7p\2\2\u024a\u024b\7u\2\2\u024b")
        buf.write("\u024c\7v\2\2\u024c\u009a\3\2\2\2\u024d\u024e\7c\2\2\u024e")
        buf.write("\u024f\7y\2\2\u024f\u0250\7c\2\2\u0250\u0251\7k\2\2\u0251")
        buf.write("\u0252\7v\2\2\u0252\u009c\3\2\2\2\u0253\u0254\7c\2\2\u0254")
        buf.write("\u0255\7u\2\2\u0255\u0256\7u\2\2\u0256\u0257\7g\2\2\u0257")
        buf.write("\u0258\7t\2\2\u0258\u0259\7v\2\2\u0259\u009e\3\2\2\2\u025a")
        buf.write("\u025b\7x\2\2\u025b\u025c\7c\2\2\u025c\u025d\7t\2\2\u025d")
        buf.write("\u00a0\3\2\2\2\u025e\u025f\7v\2\2\u025f\u0260\7t\2\2\u0260")
        buf.write("\u0261\7c\2\2\u0261\u0262\7r\2\2\u0262\u00a2\3\2\2\2\u0263")
        buf.write("\u0264\7r\2\2\u0264\u0265\7q\2\2\u0265\u0266\7u\2\2\u0266")
        buf.write("\u0267\7u\2\2\u0267\u0268\7k\2\2\u0268\u0269\7d\2\2\u0269")
        buf.write("\u026a\7n\2\2\u026a\u026b\7{\2\2\u026b\u00a4\3\2\2\2\u026c")
        buf.write("\u026d\7r\2\2\u026d\u026e\7c\2\2\u026e\u026f\7u\2\2\u026f")
        buf.write("\u0270\7u\2\2\u0270\u00a6\3\2\2\2\u0271\u0272\7f\2\2\u0272")
        buf.write("\u0273\7g\2\2\u0273\u0274\7n\2\2\u0274\u00a8\3\2\2\2\u0275")
        buf.write("\u0276\7u\2\2\u0276\u0277\7r\2\2\u0277\u0278\7c\2\2\u0278")
        buf.write("\u0279\7y\2\2\u0279\u027a\7p\2\2\u027a\u00aa\3\2\2\2\u027b")
        buf.write("\u027c\7k\2\2\u027c\u027d\7p\2\2\u027d\u027e\7x\2\2\u027e")
        buf.write("\u027f\7c\2\2\u027f\u0280\7t\2\2\u0280\u0281\7k\2\2\u0281")
        buf.write("\u0282\7c\2\2\u0282\u0283\7p\2\2\u0283\u0284\7v\2\2\u0284")
        buf.write("\u00ac\3\2\2\2\u0285\u0286\7i\2\2\u0286\u0287\7q\2\2\u0287")
        buf.write("\u00ae\3\2\2\2\u0288\u0289\7u\2\2\u0289\u028a\7g\2\2\u028a")
        buf.write("\u028b\7s\2\2\u028b\u028c\7w\2\2\u028c\u028d\7g\2\2\u028d")
        buf.write("\u028e\7p\2\2\u028e\u028f\7v\2\2\u028f\u0290\7k\2\2\u0290")
        buf.write("\u0291\7c\2\2\u0291\u0292\7n\2\2\u0292\u00b0\3\2\2\2\u0293")
        buf.write("\u0294\7y\2\2\u0294\u0295\7j\2\2\u0295\u0296\7g\2\2\u0296")
        buf.write("\u0297\7p\2\2\u0297\u00b2\3\2\2\2\u0298\u0299\7n\2\2\u0299")
        buf.write("\u029a\7g\2\2\u029a\u029b\7v\2\2\u029b\u00b4\3\2\2\2\u029c")
        buf.write("\u029d\7k\2\2\u029d\u029e\7h\2\2\u029e\u00b6\3\2\2\2\u029f")
        buf.write("\u02a0\7g\2\2\u02a0\u02a1\7n\2\2\u02a1\u02a2\7k\2\2\u02a2")
        buf.write("\u02a3\7h\2\2\u02a3\u00b8\3\2\2\2\u02a4\u02a5\7g\2\2\u02a5")
        buf.write("\u02a6\7n\2\2\u02a6\u02a7\7u\2\2\u02a7\u02a8\7g\2\2\u02a8")
        buf.write("\u00ba\3\2\2\2\u02a9\u02aa\7B\2\2\u02aa\u00bc\3\2\2\2")
        buf.write("\u02ab\u02ac\7y\2\2\u02ac\u02ad\7j\2\2\u02ad\u02ae\7k")
        buf.write("\2\2\u02ae\u02af\7n\2\2\u02af\u02b0\7g\2\2\u02b0\u00be")
        buf.write("\3\2\2\2\u02b1\u02b2\7f\2\2\u02b2\u02b3\7g\2\2\u02b3\u02b4")
        buf.write("\7h\2\2\u02b4\u00c0\3\2\2\2\u02b5\u02b6\7g\2\2\u02b6\u02b7")
        buf.write("\7z\2\2\u02b7\u02b8\7k\2\2\u02b8\u02b9\7u\2\2\u02b9\u02ba")
        buf.write("\7v\2\2\u02ba\u02bb\7u\2\2\u02bb\u00c2\3\2\2\2\u02bc\u02bd")
        buf.write("\7y\2\2\u02bd\u02be\7j\2\2\u02be\u02bf\7g\2\2\u02bf\u02c0")
        buf.write("\7t\2\2\u02c0\u02c1\7g\2\2\u02c1\u00c4\3\2\2\2\u02c2\u02c3")
        buf.write("\7?\2\2\u02c3\u00c6\3\2\2\2\u02c4\u02c5\7h\2\2\u02c5\u02c6")
        buf.write("\7q\2\2\u02c6\u02c7\7t\2\2\u02c7\u02c8\3\2\2\2\u02c8\u02c9")
        buf.write("\bd\4\2\u02c9\u00c8\3\2\2\2\u02ca\u02cb\7k\2\2\u02cb\u02cc")
        buf.write("\7p\2\2\u02cc\u02cd\3\2\2\2\u02cd\u02ce\be\5\2\u02ce\u00ca")
        buf.write("\3\2\2\2\u02cf\u02d0\7<\2\2\u02d0\u00cc\3\2\2\2\u02d1")
        buf.write("\u02d2\7P\2\2\u02d2\u02d3\7q\2\2\u02d3\u02d4\7p\2\2\u02d4")
        buf.write("\u02d5\7g\2\2\u02d5\u00ce\3\2\2\2\u02d6\u02d7\7c\2\2\u02d7")
        buf.write("\u02d8\7v\2\2\u02d8\u02d9\7q\2\2\u02d9\u02da\7o\2\2\u02da")
        buf.write("\u02db\7k\2\2\u02db\u02dc\7e\2\2\u02dc\u02dd\7c\2\2\u02dd")
        buf.write("\u02de\7n\2\2\u02de\u02df\7n\2\2\u02df\u02e0\7{\2\2\u02e0")
        buf.write("\u00d0\3\2\2\2\u02e1\u02e2\7H\2\2\u02e2\u02e3\7c\2\2\u02e3")
        buf.write("\u02e4\7n\2\2\u02e4\u02e5\7u\2\2\u02e5\u02eb\7g\2\2\u02e6")
        buf.write("\u02e7\7V\2\2\u02e7\u02e8\7t\2\2\u02e8\u02e9\7w\2\2\u02e9")
        buf.write("\u02eb\7g\2\2\u02ea\u02e1\3\2\2\2\u02ea\u02e6\3\2\2\2")
        buf.write("\u02eb\u00d2\3\2\2\2\u02ec\u02ed\7g\2\2\u02ed\u02ee\7")
        buf.write("v\2\2\u02ee\u02ef\7g\2\2\u02ef\u02f0\7t\2\2\u02f0\u02f1")
        buf.write("\7p\2\2\u02f1\u02f2\7c\2\2\u02f2\u02f3\7n\2\2\u02f3\u00d4")
        buf.write("\3\2\2\2\u02f4\u02f6\t\4\2\2\u02f5\u02f4\3\2\2\2\u02f6")
        buf.write("\u02f7\3\2\2\2\u02f7\u02f5\3\2\2\2\u02f7\u02f8\3\2\2\2")
        buf.write("\u02f8\u02fd\3\2\2\2\u02f9\u02fa\7k\2\2\u02fa\u02fb\7")
        buf.write("p\2\2\u02fb\u02fd\7h\2\2\u02fc\u02f5\3\2\2\2\u02fc\u02f9")
        buf.write("\3\2\2\2\u02fd\u00d6\3\2\2\2\u02fe\u0302\t\5\2\2\u02ff")
        buf.write("\u0301\t\6\2\2\u0300\u02ff\3\2\2\2\u0301\u0304\3\2\2\2")
        buf.write("\u0302\u0300\3\2\2\2\u0302\u0303\3\2\2\2\u0303\u00d8\3")
        buf.write("\2\2\2\u0304\u0302\3\2\2\2\u0305\u0308\t\7\2\2\u0306\u0309")
        buf.write("\5\u00dbn\2\u0307\u0309\5\u00d7l\2\u0308\u0306\3\2\2\2")
        buf.write("\u0308\u0307\3\2\2\2\u0309\u00da\3\2\2\2\u030a\u030b\7")
        buf.write("\62\2\2\u030b\u030c\7Z\2\2\u030c\u030e\3\2\2\2\u030d\u030f")
        buf.write("\5\u00ddo\2\u030e\u030d\3\2\2\2\u030f\u0310\3\2\2\2\u0310")
        buf.write("\u030e\3\2\2\2\u0310\u0311\3\2\2\2\u0311\u00dc\3\2\2\2")
        buf.write("\u0312\u0313\t\b\2\2\u0313\u00de\3\2\2\2\u0314\u0315\7")
        buf.write("]\2\2\u0315\u0316\bp\6\2\u0316\u00e0\3\2\2\2\u0317\u0318")
        buf.write("\7_\2\2\u0318\u0319\bq\7\2\u0319\u00e2\3\2\2\2\u031a\u031b")
        buf.write("\7}\2\2\u031b\u031c\br\b\2\u031c\u00e4\3\2\2\2\u031d\u031e")
        buf.write("\7\177\2\2\u031e\u031f\bs\t\2\u031f\u00e6\3\2\2\2\u0320")
        buf.write("\u0321\7*\2\2\u0321\u0322\bt\n\2\u0322\u00e8\3\2\2\2\u0323")
        buf.write("\u0324\7+\2\2\u0324\u0325\bu\13\2\u0325\u00ea\3\2\2\2")
        buf.write("\u0326\u0327\7=\2\2\u0327\u00ec\3\2\2\2\u0328\u032b\5")
        buf.write("\u00efx\2\u0329\u032b\5\u00f1y\2\u032a\u0328\3\2\2\2\u032a")
        buf.write("\u0329\3\2\2\2\u032b\u00ee\3\2\2\2\u032c\u0331\7)\2\2")
        buf.write("\u032d\u0330\5\u00f7|\2\u032e\u0330\n\t\2\2\u032f\u032d")
        buf.write("\3\2\2\2\u032f\u032e\3\2\2\2\u0330\u0333\3\2\2\2\u0331")
        buf.write("\u032f\3\2\2\2\u0331\u0332\3\2\2\2\u0332\u0334\3\2\2\2")
        buf.write("\u0333\u0331\3\2\2\2\u0334\u033f\7)\2\2\u0335\u033a\7")
        buf.write("$\2\2\u0336\u0339\5\u00f7|\2\u0337\u0339\n\n\2\2\u0338")
        buf.write("\u0336\3\2\2\2\u0338\u0337\3\2\2\2\u0339\u033c\3\2\2\2")
        buf.write("\u033a\u0338\3\2\2\2\u033a\u033b\3\2\2\2\u033b\u033d\3")
        buf.write("\2\2\2\u033c\u033a\3\2\2\2\u033d\u033f\7$\2\2\u033e\u032c")
        buf.write("\3\2\2\2\u033e\u0335\3\2\2\2\u033f\u00f0\3\2\2\2\u0340")
        buf.write("\u0341\7)\2\2\u0341\u0342\7)\2\2\u0342\u0343\7)\2\2\u0343")
        buf.write("\u0347\3\2\2\2\u0344\u0346\5\u00f3z\2\u0345\u0344\3\2")
        buf.write("\2\2\u0346\u0349\3\2\2\2\u0347\u0348\3\2\2\2\u0347\u0345")
        buf.write("\3\2\2\2\u0348\u034a\3\2\2\2\u0349\u0347\3\2\2\2\u034a")
        buf.write("\u034b\7)\2\2\u034b\u034c\7)\2\2\u034c\u035b\7)\2\2\u034d")
        buf.write("\u034e\7$\2\2\u034e\u034f\7$\2\2\u034f\u0350\7$\2\2\u0350")
        buf.write("\u0354\3\2\2\2\u0351\u0353\5\u00f3z\2\u0352\u0351\3\2")
        buf.write("\2\2\u0353\u0356\3\2\2\2\u0354\u0355\3\2\2\2\u0354\u0352")
        buf.write("\3\2\2\2\u0355\u0357\3\2\2\2\u0356\u0354\3\2\2\2\u0357")
        buf.write("\u0358\7$\2\2\u0358\u0359\7$\2\2\u0359\u035b\7$\2\2\u035a")
        buf.write("\u0340\3\2\2\2\u035a\u034d\3\2\2\2\u035b\u00f2\3\2\2\2")
        buf.write("\u035c\u035f\5\u00f5{\2\u035d\u035f\5\u00f7|\2\u035e\u035c")
        buf.write("\3\2\2\2\u035e\u035d\3\2\2\2\u035f\u00f4\3\2\2\2\u0360")
        buf.write("\u0361\n\13\2\2\u0361\u00f6\3\2\2\2\u0362\u0363\7^\2\2")
        buf.write("\u0363\u0367\13\2\2\2\u0364\u0365\7^\2\2\u0365\u0367\5")
        buf.write("m\67\2\u0366\u0362\3\2\2\2\u0366\u0364\3\2\2\2\u0367\u00f8")
        buf.write("\3\2\2\2\34\2\u01cb\u01d1\u01d9\u01de\u01e3\u01eb\u01f4")
        buf.write("\u01f7\u02ea\u02f7\u02fc\u0302\u0308\u0310\u032a\u032f")
        buf.write("\u0331\u0338\u033a\u033e\u0347\u0354\u035a\u035e\u0366")
        buf.write("\f\3\67\2\b\2\2\3d\3\3e\4\3p\5\3q\6\3r\7\3s\b\3t\t\3u")
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
    NL = 54
    WS = 55
    COMMENT_START = 56
    OPEN_MULTI_COMMENT = 57
    CLOSE_MULTI_COMMENT = 58
    POINTER_OF = 59
    STAR = 60
    AS = 61
    DOT = 62
    IMPORT = 63
    PRINT = 64
    FROM = 65
    RANGE = 66
    SETINTLEVEL = 67
    ARROW = 68
    SAVE = 69
    STOP = 70
    LAMBDA = 71
    ADDRESS_OF = 72
    NOT = 73
    COMMA = 74
    CONST = 75
    AWAIT = 76
    ASSERT = 77
    VAR = 78
    TRAP = 79
    POSSIBLY = 80
    PASS = 81
    DEL = 82
    SPAWN = 83
    INVARIANT = 84
    GO = 85
    SEQUENTIAL = 86
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
            "'and'", "'or'", "'=>'", "'&'", "'|'", "'^'", "'-'", "'+'", 
            "'//'", "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", 
            "'!='", "'<'", "'<='", "'>'", "'>='", "'~'", "'abs'", "'atLabel'", 
            "'countLabel'", "'get_context'", "'contexts'", "'isEmpty'", 
            "'min'", "'max'", "'len'", "'str'", "'any'", "'all'", "'keys'", 
            "'hash'", "'choose'", "'end'", "'and='", "'or='", "'=>='", "'&='", 
            "'|='", "'^='", "'-='", "'+='", "'*='", "'/='", "'//='", "'%='", 
            "'mod='", "'**='", "'>>='", "'#'", "'(*'", "'*)'", "'!'", "'*'", 
            "'as'", "'.'", "'import'", "'print'", "'from'", "'..'", "'setintlevel'", 
            "'->'", "'save'", "'stop'", "'lambda'", "'?'", "'not'", "','", 
            "'const'", "'await'", "'assert'", "'var'", "'trap'", "'possibly'", 
            "'pass'", "'del'", "'spawn'", "'invariant'", "'go'", "'sequential'", 
            "'when'", "'let'", "'if'", "'elif'", "'else'", "'@'", "'while'", 
            "'def'", "'exists'", "'where'", "'='", "'for'", "'in'", "':'", 
            "'None'", "'atomically'", "'eternal'", "'['", "']'", "'{'", 
            "'}'", "'('", "')'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "NL", "WS", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
            "POINTER_OF", "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", 
            "RANGE", "SETINTLEVEL", "ARROW", "SAVE", "STOP", "LAMBDA", "ADDRESS_OF", 
            "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", "VAR", "TRAP", "POSSIBLY", 
            "PASS", "DEL", "SPAWN", "INVARIANT", "GO", "SEQUENTIAL", "WHEN", 
            "LET", "IF", "ELIF", "ELSE", "AT", "WHILE", "DEF", "EXISTS", 
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
                  "T__50", "T__51", "T__52", "NL", "WS", "COMMENT", "COMMENT_START", 
                  "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", "POINTER_OF", 
                  "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", "RANGE", 
                  "SETINTLEVEL", "ARROW", "SAVE", "STOP", "LAMBDA", "ADDRESS_OF", 
                  "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", "VAR", "TRAP", 
                  "POSSIBLY", "PASS", "DEL", "SPAWN", "INVARIANT", "GO", 
                  "SEQUENTIAL", "WHEN", "LET", "IF", "ELIF", "ELSE", "AT", 
                  "WHILE", "DEF", "EXISTS", "WHERE", "EQ", "FOR", "IN", 
                  "COLON", "NONE", "ATOMICALLY", "BOOL", "ETERNAL", "INT", 
                  "NAME", "ATOM", "HEX_INTEGER", "HEX_DIGIT", "OPEN_BRACK", 
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
            actions[53] = self.NL_action 
            actions[98] = self.FOR_action 
            actions[99] = self.IN_action 
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
     


