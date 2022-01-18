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
        buf.write("\u0366\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("y\ty\4z\tz\4{\t{\4|\t|\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3")
        buf.write("\3\4\3\4\3\4\3\5\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3")
        buf.write("\t\3\n\3\n\3\13\3\13\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3")
        buf.write("\16\3\16\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\22\3\22\3\22\3\23\3\23\3\23\3\24\3\24\3\25\3\25\3\25")
        buf.write("\3\26\3\26\3\27\3\27\3\27\3\30\3\30\3\31\3\31\3\31\3\31")
        buf.write("\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\33\3\33\3\33")
        buf.write("\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\35\3\35")
        buf.write("\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3")
        buf.write("!\3!\3!\3!\3\"\3\"\3\"\3\"\3#\3#\3#\3#\3$\3$\3$\3$\3%")
        buf.write("\3%\3%\3%\3%\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3")
        buf.write("\'\3(\3(\3(\3(\3)\3)\3)\3)\3)\3*\3*\3*\3*\3+\3+\3+\3+")
        buf.write("\3,\3,\3,\3-\3-\3-\3.\3.\3.\3/\3/\3/\3\60\3\60\3\60\3")
        buf.write("\61\3\61\3\61\3\62\3\62\3\62\3\63\3\63\3\63\3\63\3\64")
        buf.write("\3\64\3\64\3\65\3\65\3\65\3\65\3\65\3\66\3\66\3\66\3\66")
        buf.write("\3\67\3\67\3\67\3\67\38\58\u01d0\n8\38\38\78\u01d4\n8")
        buf.write("\f8\168\u01d7\138\38\58\u01da\n8\38\38\39\69\u01df\n9")
        buf.write("\r9\169\u01e0\39\39\39\39\59\u01e7\n9\39\39\3:\3:\7:\u01ed")
        buf.write("\n:\f:\16:\u01f0\13:\3:\3:\3:\3:\7:\u01f6\n:\f:\16:\u01f9")
        buf.write("\13:\5:\u01fb\n:\3;\3;\3<\3<\3<\3=\3=\3=\3>\3>\3?\3?\3")
        buf.write("@\3@\3@\3A\3A\3B\3B\3B\3B\3B\3B\3B\3C\3C\3C\3C\3C\3C\3")
        buf.write("D\3D\3D\3D\3D\3E\3E\3E\3F\3F\3F\3F\3F\3F\3F\3F\3F\3F\3")
        buf.write("F\3F\3G\3G\3G\3H\3H\3H\3H\3H\3I\3I\3I\3I\3I\3I\3I\3J\3")
        buf.write("J\3K\3K\3K\3K\3L\3L\3M\3M\3M\3M\3M\3M\3N\3N\3N\3N\3N\3")
        buf.write("N\3O\3O\3O\3O\3O\3O\3O\3P\3P\3P\3P\3Q\3Q\3Q\3Q\3Q\3R\3")
        buf.write("R\3R\3R\3R\3R\3R\3R\3R\3S\3S\3S\3S\3S\3T\3T\3T\3T\3U\3")
        buf.write("U\3U\3U\3U\3U\3V\3V\3V\3V\3V\3V\3V\3V\3V\3V\3W\3W\3W\3")
        buf.write("X\3X\3X\3X\3X\3X\3X\3X\3X\3X\3X\3Y\3Y\3Y\3Y\3Y\3Z\3Z\3")
        buf.write("Z\3Z\3[\3[\3[\3\\\3\\\3\\\3\\\3\\\3]\3]\3]\3]\3]\3^\3")
        buf.write("^\3_\3_\3_\3_\3_\3_\3`\3`\3`\3`\3a\3a\3a\3a\3a\3a\3a\3")
        buf.write("b\3b\3b\3b\3b\3b\3c\3c\3d\3d\3d\3d\3d\3d\3e\3e\3e\3e\3")
        buf.write("e\3f\3f\3g\3g\3g\3g\3g\3h\3h\3h\3h\3h\3h\3h\3h\3h\3h\3")
        buf.write("h\3i\3i\3i\3i\3i\3i\3i\3i\3i\5i\u02e9\ni\3j\3j\3j\3j\3")
        buf.write("j\3j\3j\3j\3k\6k\u02f4\nk\rk\16k\u02f5\3k\3k\3k\5k\u02fb")
        buf.write("\nk\3l\3l\7l\u02ff\nl\fl\16l\u0302\13l\3m\3m\3m\5m\u0307")
        buf.write("\nm\3n\3n\3n\3n\6n\u030d\nn\rn\16n\u030e\3o\3o\3p\3p\3")
        buf.write("p\3q\3q\3q\3r\3r\3r\3s\3s\3s\3t\3t\3t\3u\3u\3u\3v\3v\3")
        buf.write("w\3w\5w\u0329\nw\3x\3x\3x\7x\u032e\nx\fx\16x\u0331\13")
        buf.write("x\3x\3x\3x\3x\7x\u0337\nx\fx\16x\u033a\13x\3x\5x\u033d")
        buf.write("\nx\3y\3y\3y\3y\3y\7y\u0344\ny\fy\16y\u0347\13y\3y\3y")
        buf.write("\3y\3y\3y\3y\3y\3y\7y\u0351\ny\fy\16y\u0354\13y\3y\3y")
        buf.write("\3y\5y\u0359\ny\3z\3z\5z\u035d\nz\3{\3{\3|\3|\3|\3|\5")
        buf.write("|\u0365\n|\5\u01ee\u0345\u0352\2}\3\3\5\4\7\5\t\6\13\7")
        buf.write("\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21")
        buf.write("!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67")
        buf.write("\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61")
        buf.write("a\62c\63e\64g\65i\66k\67m8o9q:s\2u;w<y={>}?\177@\u0081")
        buf.write("A\u0083B\u0085C\u0087D\u0089E\u008bF\u008dG\u008fH\u0091")
        buf.write("I\u0093J\u0095K\u0097L\u0099M\u009bN\u009dO\u009fP\u00a1")
        buf.write("Q\u00a3R\u00a5S\u00a7T\u00a9U\u00abV\u00adW\u00afX\u00b1")
        buf.write("Y\u00b3Z\u00b5[\u00b7\\\u00b9]\u00bb^\u00bd_\u00bf`\u00c1")
        buf.write("a\u00c3b\u00c5c\u00c7d\u00c9e\u00cbf\u00cdg\u00cfh\u00d1")
        buf.write("i\u00d3j\u00d5k\u00d7l\u00d9m\u00dbn\u00dd\2\u00dfo\u00e1")
        buf.write("p\u00e3q\u00e5r\u00e7s\u00e9t\u00ebu\u00edv\u00ef\2\u00f1")
        buf.write("\2\u00f3\2\u00f5\2\u00f7\2\3\2\13\4\2\f\f\16\17\3\2\62")
        buf.write(";\5\2C\\aac|\6\2\62;C\\aac|\3\2\60\60\5\2\62;CHch\6\2")
        buf.write("\f\f\16\17))^^\6\2\f\f\16\17$$^^\3\2^^\2\u0379\2\3\3\2")
        buf.write("\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2")
        buf.write("\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2")
        buf.write("\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35")
        buf.write("\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2")
        buf.write("\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2")
        buf.write("\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2")
        buf.write("\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2")
        buf.write("\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2")
        buf.write("\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3")
        buf.write("\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_")
        buf.write("\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2")
        buf.write("i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2")
        buf.write("\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2")
        buf.write("\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085")
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
        buf.write("\3\2\2\2\2\u00db\3\2\2\2\2\u00df\3\2\2\2\2\u00e1\3\2\2")
        buf.write("\2\2\u00e3\3\2\2\2\2\u00e5\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9")
        buf.write("\3\2\2\2\2\u00eb\3\2\2\2\2\u00ed\3\2\2\2\3\u00f9\3\2\2")
        buf.write("\2\5\u00fd\3\2\2\2\7\u0101\3\2\2\2\t\u0104\3\2\2\2\13")
        buf.write("\u0107\3\2\2\2\r\u0109\3\2\2\2\17\u010b\3\2\2\2\21\u010d")
        buf.write("\3\2\2\2\23\u010f\3\2\2\2\25\u0111\3\2\2\2\27\u0114\3")
        buf.write("\2\2\2\31\u0116\3\2\2\2\33\u0118\3\2\2\2\35\u011c\3\2")
        buf.write("\2\2\37\u011f\3\2\2\2!\u0122\3\2\2\2#\u0125\3\2\2\2%\u0128")
        buf.write("\3\2\2\2\'\u012b\3\2\2\2)\u012d\3\2\2\2+\u0130\3\2\2\2")
        buf.write("-\u0132\3\2\2\2/\u0135\3\2\2\2\61\u0137\3\2\2\2\63\u013b")
        buf.write("\3\2\2\2\65\u0143\3\2\2\2\67\u014e\3\2\2\29\u015a\3\2")
        buf.write("\2\2;\u0163\3\2\2\2=\u016b\3\2\2\2?\u016f\3\2\2\2A\u0173")
        buf.write("\3\2\2\2C\u0177\3\2\2\2E\u017b\3\2\2\2G\u017f\3\2\2\2")
        buf.write("I\u0183\3\2\2\2K\u0188\3\2\2\2M\u018d\3\2\2\2O\u0194\3")
        buf.write("\2\2\2Q\u0198\3\2\2\2S\u019d\3\2\2\2U\u01a1\3\2\2\2W\u01a5")
        buf.write("\3\2\2\2Y\u01a8\3\2\2\2[\u01ab\3\2\2\2]\u01ae\3\2\2\2")
        buf.write("_\u01b1\3\2\2\2a\u01b4\3\2\2\2c\u01b7\3\2\2\2e\u01ba\3")
        buf.write("\2\2\2g\u01be\3\2\2\2i\u01c1\3\2\2\2k\u01c6\3\2\2\2m\u01ca")
        buf.write("\3\2\2\2o\u01cf\3\2\2\2q\u01e6\3\2\2\2s\u01fa\3\2\2\2")
        buf.write("u\u01fc\3\2\2\2w\u01fe\3\2\2\2y\u0201\3\2\2\2{\u0204\3")
        buf.write("\2\2\2}\u0206\3\2\2\2\177\u0208\3\2\2\2\u0081\u020b\3")
        buf.write("\2\2\2\u0083\u020d\3\2\2\2\u0085\u0214\3\2\2\2\u0087\u021a")
        buf.write("\3\2\2\2\u0089\u021f\3\2\2\2\u008b\u0222\3\2\2\2\u008d")
        buf.write("\u022e\3\2\2\2\u008f\u0231\3\2\2\2\u0091\u0236\3\2\2\2")
        buf.write("\u0093\u023d\3\2\2\2\u0095\u023f\3\2\2\2\u0097\u0243\3")
        buf.write("\2\2\2\u0099\u0245\3\2\2\2\u009b\u024b\3\2\2\2\u009d\u0251")
        buf.write("\3\2\2\2\u009f\u0258\3\2\2\2\u00a1\u025c\3\2\2\2\u00a3")
        buf.write("\u0261\3\2\2\2\u00a5\u026a\3\2\2\2\u00a7\u026f\3\2\2\2")
        buf.write("\u00a9\u0273\3\2\2\2\u00ab\u0279\3\2\2\2\u00ad\u0283\3")
        buf.write("\2\2\2\u00af\u0286\3\2\2\2\u00b1\u0291\3\2\2\2\u00b3\u0296")
        buf.write("\3\2\2\2\u00b5\u029a\3\2\2\2\u00b7\u029d\3\2\2\2\u00b9")
        buf.write("\u02a2\3\2\2\2\u00bb\u02a7\3\2\2\2\u00bd\u02a9\3\2\2\2")
        buf.write("\u00bf\u02af\3\2\2\2\u00c1\u02b3\3\2\2\2\u00c3\u02ba\3")
        buf.write("\2\2\2\u00c5\u02c0\3\2\2\2\u00c7\u02c2\3\2\2\2\u00c9\u02c8")
        buf.write("\3\2\2\2\u00cb\u02cd\3\2\2\2\u00cd\u02cf\3\2\2\2\u00cf")
        buf.write("\u02d4\3\2\2\2\u00d1\u02e8\3\2\2\2\u00d3\u02ea\3\2\2\2")
        buf.write("\u00d5\u02fa\3\2\2\2\u00d7\u02fc\3\2\2\2\u00d9\u0303\3")
        buf.write("\2\2\2\u00db\u0308\3\2\2\2\u00dd\u0310\3\2\2\2\u00df\u0312")
        buf.write("\3\2\2\2\u00e1\u0315\3\2\2\2\u00e3\u0318\3\2\2\2\u00e5")
        buf.write("\u031b\3\2\2\2\u00e7\u031e\3\2\2\2\u00e9\u0321\3\2\2\2")
        buf.write("\u00eb\u0324\3\2\2\2\u00ed\u0328\3\2\2\2\u00ef\u033c\3")
        buf.write("\2\2\2\u00f1\u0358\3\2\2\2\u00f3\u035c\3\2\2\2\u00f5\u035e")
        buf.write("\3\2\2\2\u00f7\u0364\3\2\2\2\u00f9\u00fa\7\60\2\2\u00fa")
        buf.write("\u00fb\7\60\2\2\u00fb\u00fc\7\60\2\2\u00fc\4\3\2\2\2\u00fd")
        buf.write("\u00fe\7c\2\2\u00fe\u00ff\7p\2\2\u00ff\u0100\7f\2\2\u0100")
        buf.write("\6\3\2\2\2\u0101\u0102\7q\2\2\u0102\u0103\7t\2\2\u0103")
        buf.write("\b\3\2\2\2\u0104\u0105\7?\2\2\u0105\u0106\7@\2\2\u0106")
        buf.write("\n\3\2\2\2\u0107\u0108\7(\2\2\u0108\f\3\2\2\2\u0109\u010a")
        buf.write("\7~\2\2\u010a\16\3\2\2\2\u010b\u010c\7`\2\2\u010c\20\3")
        buf.write("\2\2\2\u010d\u010e\7/\2\2\u010e\22\3\2\2\2\u010f\u0110")
        buf.write("\7-\2\2\u0110\24\3\2\2\2\u0111\u0112\7\61\2\2\u0112\u0113")
        buf.write("\7\61\2\2\u0113\26\3\2\2\2\u0114\u0115\7\61\2\2\u0115")
        buf.write("\30\3\2\2\2\u0116\u0117\7\'\2\2\u0117\32\3\2\2\2\u0118")
        buf.write("\u0119\7o\2\2\u0119\u011a\7q\2\2\u011a\u011b\7f\2\2\u011b")
        buf.write("\34\3\2\2\2\u011c\u011d\7,\2\2\u011d\u011e\7,\2\2\u011e")
        buf.write("\36\3\2\2\2\u011f\u0120\7>\2\2\u0120\u0121\7>\2\2\u0121")
        buf.write(" \3\2\2\2\u0122\u0123\7@\2\2\u0123\u0124\7@\2\2\u0124")
        buf.write("\"\3\2\2\2\u0125\u0126\7?\2\2\u0126\u0127\7?\2\2\u0127")
        buf.write("$\3\2\2\2\u0128\u0129\7#\2\2\u0129\u012a\7?\2\2\u012a")
        buf.write("&\3\2\2\2\u012b\u012c\7>\2\2\u012c(\3\2\2\2\u012d\u012e")
        buf.write("\7>\2\2\u012e\u012f\7?\2\2\u012f*\3\2\2\2\u0130\u0131")
        buf.write("\7@\2\2\u0131,\3\2\2\2\u0132\u0133\7@\2\2\u0133\u0134")
        buf.write("\7?\2\2\u0134.\3\2\2\2\u0135\u0136\7\u0080\2\2\u0136\60")
        buf.write("\3\2\2\2\u0137\u0138\7c\2\2\u0138\u0139\7d\2\2\u0139\u013a")
        buf.write("\7u\2\2\u013a\62\3\2\2\2\u013b\u013c\7c\2\2\u013c\u013d")
        buf.write("\7v\2\2\u013d\u013e\7N\2\2\u013e\u013f\7c\2\2\u013f\u0140")
        buf.write("\7d\2\2\u0140\u0141\7g\2\2\u0141\u0142\7n\2\2\u0142\64")
        buf.write("\3\2\2\2\u0143\u0144\7e\2\2\u0144\u0145\7q\2\2\u0145\u0146")
        buf.write("\7w\2\2\u0146\u0147\7p\2\2\u0147\u0148\7v\2\2\u0148\u0149")
        buf.write("\7N\2\2\u0149\u014a\7c\2\2\u014a\u014b\7d\2\2\u014b\u014c")
        buf.write("\7g\2\2\u014c\u014d\7n\2\2\u014d\66\3\2\2\2\u014e\u014f")
        buf.write("\7i\2\2\u014f\u0150\7g\2\2\u0150\u0151\7v\2\2\u0151\u0152")
        buf.write("\7a\2\2\u0152\u0153\7e\2\2\u0153\u0154\7q\2\2\u0154\u0155")
        buf.write("\7p\2\2\u0155\u0156\7v\2\2\u0156\u0157\7g\2\2\u0157\u0158")
        buf.write("\7z\2\2\u0158\u0159\7v\2\2\u01598\3\2\2\2\u015a\u015b")
        buf.write("\7e\2\2\u015b\u015c\7q\2\2\u015c\u015d\7p\2\2\u015d\u015e")
        buf.write("\7v\2\2\u015e\u015f\7g\2\2\u015f\u0160\7z\2\2\u0160\u0161")
        buf.write("\7v\2\2\u0161\u0162\7u\2\2\u0162:\3\2\2\2\u0163\u0164")
        buf.write("\7k\2\2\u0164\u0165\7u\2\2\u0165\u0166\7G\2\2\u0166\u0167")
        buf.write("\7o\2\2\u0167\u0168\7r\2\2\u0168\u0169\7v\2\2\u0169\u016a")
        buf.write("\7{\2\2\u016a<\3\2\2\2\u016b\u016c\7o\2\2\u016c\u016d")
        buf.write("\7k\2\2\u016d\u016e\7p\2\2\u016e>\3\2\2\2\u016f\u0170")
        buf.write("\7o\2\2\u0170\u0171\7c\2\2\u0171\u0172\7z\2\2\u0172@\3")
        buf.write("\2\2\2\u0173\u0174\7n\2\2\u0174\u0175\7g\2\2\u0175\u0176")
        buf.write("\7p\2\2\u0176B\3\2\2\2\u0177\u0178\7u\2\2\u0178\u0179")
        buf.write("\7v\2\2\u0179\u017a\7t\2\2\u017aD\3\2\2\2\u017b\u017c")
        buf.write("\7c\2\2\u017c\u017d\7p\2\2\u017d\u017e\7{\2\2\u017eF\3")
        buf.write("\2\2\2\u017f\u0180\7c\2\2\u0180\u0181\7n\2\2\u0181\u0182")
        buf.write("\7n\2\2\u0182H\3\2\2\2\u0183\u0184\7m\2\2\u0184\u0185")
        buf.write("\7g\2\2\u0185\u0186\7{\2\2\u0186\u0187\7u\2\2\u0187J\3")
        buf.write("\2\2\2\u0188\u0189\7j\2\2\u0189\u018a\7c\2\2\u018a\u018b")
        buf.write("\7u\2\2\u018b\u018c\7j\2\2\u018cL\3\2\2\2\u018d\u018e")
        buf.write("\7e\2\2\u018e\u018f\7j\2\2\u018f\u0190\7q\2\2\u0190\u0191")
        buf.write("\7q\2\2\u0191\u0192\7u\2\2\u0192\u0193\7g\2\2\u0193N\3")
        buf.write("\2\2\2\u0194\u0195\7g\2\2\u0195\u0196\7p\2\2\u0196\u0197")
        buf.write("\7f\2\2\u0197P\3\2\2\2\u0198\u0199\7c\2\2\u0199\u019a")
        buf.write("\7p\2\2\u019a\u019b\7f\2\2\u019b\u019c\7?\2\2\u019cR\3")
        buf.write("\2\2\2\u019d\u019e\7q\2\2\u019e\u019f\7t\2\2\u019f\u01a0")
        buf.write("\7?\2\2\u01a0T\3\2\2\2\u01a1\u01a2\7?\2\2\u01a2\u01a3")
        buf.write("\7@\2\2\u01a3\u01a4\7?\2\2\u01a4V\3\2\2\2\u01a5\u01a6")
        buf.write("\7(\2\2\u01a6\u01a7\7?\2\2\u01a7X\3\2\2\2\u01a8\u01a9")
        buf.write("\7~\2\2\u01a9\u01aa\7?\2\2\u01aaZ\3\2\2\2\u01ab\u01ac")
        buf.write("\7`\2\2\u01ac\u01ad\7?\2\2\u01ad\\\3\2\2\2\u01ae\u01af")
        buf.write("\7/\2\2\u01af\u01b0\7?\2\2\u01b0^\3\2\2\2\u01b1\u01b2")
        buf.write("\7-\2\2\u01b2\u01b3\7?\2\2\u01b3`\3\2\2\2\u01b4\u01b5")
        buf.write("\7,\2\2\u01b5\u01b6\7?\2\2\u01b6b\3\2\2\2\u01b7\u01b8")
        buf.write("\7\61\2\2\u01b8\u01b9\7?\2\2\u01b9d\3\2\2\2\u01ba\u01bb")
        buf.write("\7\61\2\2\u01bb\u01bc\7\61\2\2\u01bc\u01bd\7?\2\2\u01bd")
        buf.write("f\3\2\2\2\u01be\u01bf\7\'\2\2\u01bf\u01c0\7?\2\2\u01c0")
        buf.write("h\3\2\2\2\u01c1\u01c2\7o\2\2\u01c2\u01c3\7q\2\2\u01c3")
        buf.write("\u01c4\7f\2\2\u01c4\u01c5\7?\2\2\u01c5j\3\2\2\2\u01c6")
        buf.write("\u01c7\7,\2\2\u01c7\u01c8\7,\2\2\u01c8\u01c9\7?\2\2\u01c9")
        buf.write("l\3\2\2\2\u01ca\u01cb\7@\2\2\u01cb\u01cc\7@\2\2\u01cc")
        buf.write("\u01cd\7?\2\2\u01cdn\3\2\2\2\u01ce\u01d0\7\17\2\2\u01cf")
        buf.write("\u01ce\3\2\2\2\u01cf\u01d0\3\2\2\2\u01d0\u01d1\3\2\2\2")
        buf.write("\u01d1\u01d9\7\f\2\2\u01d2\u01d4\7\"\2\2\u01d3\u01d2\3")
        buf.write("\2\2\2\u01d4\u01d7\3\2\2\2\u01d5\u01d3\3\2\2\2\u01d5\u01d6")
        buf.write("\3\2\2\2\u01d6\u01da\3\2\2\2\u01d7\u01d5\3\2\2\2\u01d8")
        buf.write("\u01da\7\13\2\2\u01d9\u01d5\3\2\2\2\u01d9\u01d8\3\2\2")
        buf.write("\2\u01da\u01db\3\2\2\2\u01db\u01dc\b8\2\2\u01dcp\3\2\2")
        buf.write("\2\u01dd\u01df\7\"\2\2\u01de\u01dd\3\2\2\2\u01df\u01e0")
        buf.write("\3\2\2\2\u01e0\u01de\3\2\2\2\u01e0\u01e1\3\2\2\2\u01e1")
        buf.write("\u01e7\3\2\2\2\u01e2\u01e7\7\13\2\2\u01e3\u01e4\7^\2\2")
        buf.write("\u01e4\u01e7\5o8\2\u01e5\u01e7\5s:\2\u01e6\u01de\3\2\2")
        buf.write("\2\u01e6\u01e2\3\2\2\2\u01e6\u01e3\3\2\2\2\u01e6\u01e5")
        buf.write("\3\2\2\2\u01e7\u01e8\3\2\2\2\u01e8\u01e9\b9\3\2\u01e9")
        buf.write("r\3\2\2\2\u01ea\u01ee\5w<\2\u01eb\u01ed\13\2\2\2\u01ec")
        buf.write("\u01eb\3\2\2\2\u01ed\u01f0\3\2\2\2\u01ee\u01ef\3\2\2\2")
        buf.write("\u01ee\u01ec\3\2\2\2\u01ef\u01f1\3\2\2\2\u01f0\u01ee\3")
        buf.write("\2\2\2\u01f1\u01f2\5y=\2\u01f2\u01fb\3\2\2\2\u01f3\u01f7")
        buf.write("\5u;\2\u01f4\u01f6\n\2\2\2\u01f5\u01f4\3\2\2\2\u01f6\u01f9")
        buf.write("\3\2\2\2\u01f7\u01f5\3\2\2\2\u01f7\u01f8\3\2\2\2\u01f8")
        buf.write("\u01fb\3\2\2\2\u01f9\u01f7\3\2\2\2\u01fa\u01ea\3\2\2\2")
        buf.write("\u01fa\u01f3\3\2\2\2\u01fbt\3\2\2\2\u01fc\u01fd\7%\2\2")
        buf.write("\u01fdv\3\2\2\2\u01fe\u01ff\7*\2\2\u01ff\u0200\7,\2\2")
        buf.write("\u0200x\3\2\2\2\u0201\u0202\7,\2\2\u0202\u0203\7+\2\2")
        buf.write("\u0203z\3\2\2\2\u0204\u0205\7#\2\2\u0205|\3\2\2\2\u0206")
        buf.write("\u0207\7,\2\2\u0207~\3\2\2\2\u0208\u0209\7c\2\2\u0209")
        buf.write("\u020a\7u\2\2\u020a\u0080\3\2\2\2\u020b\u020c\7\60\2\2")
        buf.write("\u020c\u0082\3\2\2\2\u020d\u020e\7k\2\2\u020e\u020f\7")
        buf.write("o\2\2\u020f\u0210\7r\2\2\u0210\u0211\7q\2\2\u0211\u0212")
        buf.write("\7t\2\2\u0212\u0213\7v\2\2\u0213\u0084\3\2\2\2\u0214\u0215")
        buf.write("\7r\2\2\u0215\u0216\7t\2\2\u0216\u0217\7k\2\2\u0217\u0218")
        buf.write("\7p\2\2\u0218\u0219\7v\2\2\u0219\u0086\3\2\2\2\u021a\u021b")
        buf.write("\7h\2\2\u021b\u021c\7t\2\2\u021c\u021d\7q\2\2\u021d\u021e")
        buf.write("\7o\2\2\u021e\u0088\3\2\2\2\u021f\u0220\7\60\2\2\u0220")
        buf.write("\u0221\7\60\2\2\u0221\u008a\3\2\2\2\u0222\u0223\7u\2\2")
        buf.write("\u0223\u0224\7g\2\2\u0224\u0225\7v\2\2\u0225\u0226\7k")
        buf.write("\2\2\u0226\u0227\7p\2\2\u0227\u0228\7v\2\2\u0228\u0229")
        buf.write("\7n\2\2\u0229\u022a\7g\2\2\u022a\u022b\7x\2\2\u022b\u022c")
        buf.write("\7g\2\2\u022c\u022d\7n\2\2\u022d\u008c\3\2\2\2\u022e\u022f")
        buf.write("\7/\2\2\u022f\u0230\7@\2\2\u0230\u008e\3\2\2\2\u0231\u0232")
        buf.write("\7u\2\2\u0232\u0233\7v\2\2\u0233\u0234\7q\2\2\u0234\u0235")
        buf.write("\7r\2\2\u0235\u0090\3\2\2\2\u0236\u0237\7n\2\2\u0237\u0238")
        buf.write("\7c\2\2\u0238\u0239\7o\2\2\u0239\u023a\7d\2\2\u023a\u023b")
        buf.write("\7f\2\2\u023b\u023c\7c\2\2\u023c\u0092\3\2\2\2\u023d\u023e")
        buf.write("\7A\2\2\u023e\u0094\3\2\2\2\u023f\u0240\7p\2\2\u0240\u0241")
        buf.write("\7q\2\2\u0241\u0242\7v\2\2\u0242\u0096\3\2\2\2\u0243\u0244")
        buf.write("\7.\2\2\u0244\u0098\3\2\2\2\u0245\u0246\7e\2\2\u0246\u0247")
        buf.write("\7q\2\2\u0247\u0248\7p\2\2\u0248\u0249\7u\2\2\u0249\u024a")
        buf.write("\7v\2\2\u024a\u009a\3\2\2\2\u024b\u024c\7c\2\2\u024c\u024d")
        buf.write("\7y\2\2\u024d\u024e\7c\2\2\u024e\u024f\7k\2\2\u024f\u0250")
        buf.write("\7v\2\2\u0250\u009c\3\2\2\2\u0251\u0252\7c\2\2\u0252\u0253")
        buf.write("\7u\2\2\u0253\u0254\7u\2\2\u0254\u0255\7g\2\2\u0255\u0256")
        buf.write("\7t\2\2\u0256\u0257\7v\2\2\u0257\u009e\3\2\2\2\u0258\u0259")
        buf.write("\7x\2\2\u0259\u025a\7c\2\2\u025a\u025b\7t\2\2\u025b\u00a0")
        buf.write("\3\2\2\2\u025c\u025d\7v\2\2\u025d\u025e\7t\2\2\u025e\u025f")
        buf.write("\7c\2\2\u025f\u0260\7r\2\2\u0260\u00a2\3\2\2\2\u0261\u0262")
        buf.write("\7r\2\2\u0262\u0263\7q\2\2\u0263\u0264\7u\2\2\u0264\u0265")
        buf.write("\7u\2\2\u0265\u0266\7k\2\2\u0266\u0267\7d\2\2\u0267\u0268")
        buf.write("\7n\2\2\u0268\u0269\7{\2\2\u0269\u00a4\3\2\2\2\u026a\u026b")
        buf.write("\7r\2\2\u026b\u026c\7c\2\2\u026c\u026d\7u\2\2\u026d\u026e")
        buf.write("\7u\2\2\u026e\u00a6\3\2\2\2\u026f\u0270\7f\2\2\u0270\u0271")
        buf.write("\7g\2\2\u0271\u0272\7n\2\2\u0272\u00a8\3\2\2\2\u0273\u0274")
        buf.write("\7u\2\2\u0274\u0275\7r\2\2\u0275\u0276\7c\2\2\u0276\u0277")
        buf.write("\7y\2\2\u0277\u0278\7p\2\2\u0278\u00aa\3\2\2\2\u0279\u027a")
        buf.write("\7k\2\2\u027a\u027b\7p\2\2\u027b\u027c\7x\2\2\u027c\u027d")
        buf.write("\7c\2\2\u027d\u027e\7t\2\2\u027e\u027f\7k\2\2\u027f\u0280")
        buf.write("\7c\2\2\u0280\u0281\7p\2\2\u0281\u0282\7v\2\2\u0282\u00ac")
        buf.write("\3\2\2\2\u0283\u0284\7i\2\2\u0284\u0285\7q\2\2\u0285\u00ae")
        buf.write("\3\2\2\2\u0286\u0287\7u\2\2\u0287\u0288\7g\2\2\u0288\u0289")
        buf.write("\7s\2\2\u0289\u028a\7w\2\2\u028a\u028b\7g\2\2\u028b\u028c")
        buf.write("\7p\2\2\u028c\u028d\7v\2\2\u028d\u028e\7k\2\2\u028e\u028f")
        buf.write("\7c\2\2\u028f\u0290\7n\2\2\u0290\u00b0\3\2\2\2\u0291\u0292")
        buf.write("\7y\2\2\u0292\u0293\7j\2\2\u0293\u0294\7g\2\2\u0294\u0295")
        buf.write("\7p\2\2\u0295\u00b2\3\2\2\2\u0296\u0297\7n\2\2\u0297\u0298")
        buf.write("\7g\2\2\u0298\u0299\7v\2\2\u0299\u00b4\3\2\2\2\u029a\u029b")
        buf.write("\7k\2\2\u029b\u029c\7h\2\2\u029c\u00b6\3\2\2\2\u029d\u029e")
        buf.write("\7g\2\2\u029e\u029f\7n\2\2\u029f\u02a0\7k\2\2\u02a0\u02a1")
        buf.write("\7h\2\2\u02a1\u00b8\3\2\2\2\u02a2\u02a3\7g\2\2\u02a3\u02a4")
        buf.write("\7n\2\2\u02a4\u02a5\7u\2\2\u02a5\u02a6\7g\2\2\u02a6\u00ba")
        buf.write("\3\2\2\2\u02a7\u02a8\7B\2\2\u02a8\u00bc\3\2\2\2\u02a9")
        buf.write("\u02aa\7y\2\2\u02aa\u02ab\7j\2\2\u02ab\u02ac\7k\2\2\u02ac")
        buf.write("\u02ad\7n\2\2\u02ad\u02ae\7g\2\2\u02ae\u00be\3\2\2\2\u02af")
        buf.write("\u02b0\7f\2\2\u02b0\u02b1\7g\2\2\u02b1\u02b2\7h\2\2\u02b2")
        buf.write("\u00c0\3\2\2\2\u02b3\u02b4\7g\2\2\u02b4\u02b5\7z\2\2\u02b5")
        buf.write("\u02b6\7k\2\2\u02b6\u02b7\7u\2\2\u02b7\u02b8\7v\2\2\u02b8")
        buf.write("\u02b9\7u\2\2\u02b9\u00c2\3\2\2\2\u02ba\u02bb\7y\2\2\u02bb")
        buf.write("\u02bc\7j\2\2\u02bc\u02bd\7g\2\2\u02bd\u02be\7t\2\2\u02be")
        buf.write("\u02bf\7g\2\2\u02bf\u00c4\3\2\2\2\u02c0\u02c1\7?\2\2\u02c1")
        buf.write("\u00c6\3\2\2\2\u02c2\u02c3\7h\2\2\u02c3\u02c4\7q\2\2\u02c4")
        buf.write("\u02c5\7t\2\2\u02c5\u02c6\3\2\2\2\u02c6\u02c7\bd\4\2\u02c7")
        buf.write("\u00c8\3\2\2\2\u02c8\u02c9\7k\2\2\u02c9\u02ca\7p\2\2\u02ca")
        buf.write("\u02cb\3\2\2\2\u02cb\u02cc\be\5\2\u02cc\u00ca\3\2\2\2")
        buf.write("\u02cd\u02ce\7<\2\2\u02ce\u00cc\3\2\2\2\u02cf\u02d0\7")
        buf.write("P\2\2\u02d0\u02d1\7q\2\2\u02d1\u02d2\7p\2\2\u02d2\u02d3")
        buf.write("\7g\2\2\u02d3\u00ce\3\2\2\2\u02d4\u02d5\7c\2\2\u02d5\u02d6")
        buf.write("\7v\2\2\u02d6\u02d7\7q\2\2\u02d7\u02d8\7o\2\2\u02d8\u02d9")
        buf.write("\7k\2\2\u02d9\u02da\7e\2\2\u02da\u02db\7c\2\2\u02db\u02dc")
        buf.write("\7n\2\2\u02dc\u02dd\7n\2\2\u02dd\u02de\7{\2\2\u02de\u00d0")
        buf.write("\3\2\2\2\u02df\u02e0\7H\2\2\u02e0\u02e1\7c\2\2\u02e1\u02e2")
        buf.write("\7n\2\2\u02e2\u02e3\7u\2\2\u02e3\u02e9\7g\2\2\u02e4\u02e5")
        buf.write("\7V\2\2\u02e5\u02e6\7t\2\2\u02e6\u02e7\7w\2\2\u02e7\u02e9")
        buf.write("\7g\2\2\u02e8\u02df\3\2\2\2\u02e8\u02e4\3\2\2\2\u02e9")
        buf.write("\u00d2\3\2\2\2\u02ea\u02eb\7g\2\2\u02eb\u02ec\7v\2\2\u02ec")
        buf.write("\u02ed\7g\2\2\u02ed\u02ee\7t\2\2\u02ee\u02ef\7p\2\2\u02ef")
        buf.write("\u02f0\7c\2\2\u02f0\u02f1\7n\2\2\u02f1\u00d4\3\2\2\2\u02f2")
        buf.write("\u02f4\t\3\2\2\u02f3\u02f2\3\2\2\2\u02f4\u02f5\3\2\2\2")
        buf.write("\u02f5\u02f3\3\2\2\2\u02f5\u02f6\3\2\2\2\u02f6\u02fb\3")
        buf.write("\2\2\2\u02f7\u02f8\7k\2\2\u02f8\u02f9\7p\2\2\u02f9\u02fb")
        buf.write("\7h\2\2\u02fa\u02f3\3\2\2\2\u02fa\u02f7\3\2\2\2\u02fb")
        buf.write("\u00d6\3\2\2\2\u02fc\u0300\t\4\2\2\u02fd\u02ff\t\5\2\2")
        buf.write("\u02fe\u02fd\3\2\2\2\u02ff\u0302\3\2\2\2\u0300\u02fe\3")
        buf.write("\2\2\2\u0300\u0301\3\2\2\2\u0301\u00d8\3\2\2\2\u0302\u0300")
        buf.write("\3\2\2\2\u0303\u0306\t\6\2\2\u0304\u0307\5\u00dbn\2\u0305")
        buf.write("\u0307\5\u00d7l\2\u0306\u0304\3\2\2\2\u0306\u0305\3\2")
        buf.write("\2\2\u0307\u00da\3\2\2\2\u0308\u0309\7\62\2\2\u0309\u030a")
        buf.write("\7Z\2\2\u030a\u030c\3\2\2\2\u030b\u030d\5\u00ddo\2\u030c")
        buf.write("\u030b\3\2\2\2\u030d\u030e\3\2\2\2\u030e\u030c\3\2\2\2")
        buf.write("\u030e\u030f\3\2\2\2\u030f\u00dc\3\2\2\2\u0310\u0311\t")
        buf.write("\7\2\2\u0311\u00de\3\2\2\2\u0312\u0313\7]\2\2\u0313\u0314")
        buf.write("\bp\6\2\u0314\u00e0\3\2\2\2\u0315\u0316\7_\2\2\u0316\u0317")
        buf.write("\bq\7\2\u0317\u00e2\3\2\2\2\u0318\u0319\7}\2\2\u0319\u031a")
        buf.write("\br\b\2\u031a\u00e4\3\2\2\2\u031b\u031c\7\177\2\2\u031c")
        buf.write("\u031d\bs\t\2\u031d\u00e6\3\2\2\2\u031e\u031f\7*\2\2\u031f")
        buf.write("\u0320\bt\n\2\u0320\u00e8\3\2\2\2\u0321\u0322\7+\2\2\u0322")
        buf.write("\u0323\bu\13\2\u0323\u00ea\3\2\2\2\u0324\u0325\7=\2\2")
        buf.write("\u0325\u00ec\3\2\2\2\u0326\u0329\5\u00efx\2\u0327\u0329")
        buf.write("\5\u00f1y\2\u0328\u0326\3\2\2\2\u0328\u0327\3\2\2\2\u0329")
        buf.write("\u00ee\3\2\2\2\u032a\u032f\7)\2\2\u032b\u032e\5\u00f7")
        buf.write("|\2\u032c\u032e\n\b\2\2\u032d\u032b\3\2\2\2\u032d\u032c")
        buf.write("\3\2\2\2\u032e\u0331\3\2\2\2\u032f\u032d\3\2\2\2\u032f")
        buf.write("\u0330\3\2\2\2\u0330\u0332\3\2\2\2\u0331\u032f\3\2\2\2")
        buf.write("\u0332\u033d\7)\2\2\u0333\u0338\7$\2\2\u0334\u0337\5\u00f7")
        buf.write("|\2\u0335\u0337\n\t\2\2\u0336\u0334\3\2\2\2\u0336\u0335")
        buf.write("\3\2\2\2\u0337\u033a\3\2\2\2\u0338\u0336\3\2\2\2\u0338")
        buf.write("\u0339\3\2\2\2\u0339\u033b\3\2\2\2\u033a\u0338\3\2\2\2")
        buf.write("\u033b\u033d\7$\2\2\u033c\u032a\3\2\2\2\u033c\u0333\3")
        buf.write("\2\2\2\u033d\u00f0\3\2\2\2\u033e\u033f\7)\2\2\u033f\u0340")
        buf.write("\7)\2\2\u0340\u0341\7)\2\2\u0341\u0345\3\2\2\2\u0342\u0344")
        buf.write("\5\u00f3z\2\u0343\u0342\3\2\2\2\u0344\u0347\3\2\2\2\u0345")
        buf.write("\u0346\3\2\2\2\u0345\u0343\3\2\2\2\u0346\u0348\3\2\2\2")
        buf.write("\u0347\u0345\3\2\2\2\u0348\u0349\7)\2\2\u0349\u034a\7")
        buf.write(")\2\2\u034a\u0359\7)\2\2\u034b\u034c\7$\2\2\u034c\u034d")
        buf.write("\7$\2\2\u034d\u034e\7$\2\2\u034e\u0352\3\2\2\2\u034f\u0351")
        buf.write("\5\u00f3z\2\u0350\u034f\3\2\2\2\u0351\u0354\3\2\2\2\u0352")
        buf.write("\u0353\3\2\2\2\u0352\u0350\3\2\2\2\u0353\u0355\3\2\2\2")
        buf.write("\u0354\u0352\3\2\2\2\u0355\u0356\7$\2\2\u0356\u0357\7")
        buf.write("$\2\2\u0357\u0359\7$\2\2\u0358\u033e\3\2\2\2\u0358\u034b")
        buf.write("\3\2\2\2\u0359\u00f2\3\2\2\2\u035a\u035d\5\u00f5{\2\u035b")
        buf.write("\u035d\5\u00f7|\2\u035c\u035a\3\2\2\2\u035c\u035b\3\2")
        buf.write("\2\2\u035d\u00f4\3\2\2\2\u035e\u035f\n\n\2\2\u035f\u00f6")
        buf.write("\3\2\2\2\u0360\u0361\7^\2\2\u0361\u0365\13\2\2\2\u0362")
        buf.write("\u0363\7^\2\2\u0363\u0365\5o8\2\u0364\u0360\3\2\2\2\u0364")
        buf.write("\u0362\3\2\2\2\u0365\u00f8\3\2\2\2\34\2\u01cf\u01d5\u01d9")
        buf.write("\u01e0\u01e6\u01ee\u01f7\u01fa\u02e8\u02f5\u02fa\u0300")
        buf.write("\u0306\u030e\u0328\u032d\u032f\u0336\u0338\u033c\u0345")
        buf.write("\u0352\u0358\u035c\u0364\f\38\2\b\2\2\3d\3\3e\4\3p\5\3")
        buf.write("q\6\3r\7\3s\b\3t\t\3u\n")
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
    NL = 55
    WS = 56
    COMMENT_START = 57
    OPEN_MULTI_COMMENT = 58
    CLOSE_MULTI_COMMENT = 59
    POINTER_OF = 60
    STAR = 61
    AS = 62
    DOT = 63
    IMPORT = 64
    PRINT = 65
    FROM = 66
    RANGE = 67
    SETINTLEVEL = 68
    ARROW = 69
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
            "'...'", "'and'", "'or'", "'=>'", "'&'", "'|'", "'^'", "'-'", 
            "'+'", "'//'", "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", 
            "'=='", "'!='", "'<'", "'<='", "'>'", "'>='", "'~'", "'abs'", 
            "'atLabel'", "'countLabel'", "'get_context'", "'contexts'", 
            "'isEmpty'", "'min'", "'max'", "'len'", "'str'", "'any'", "'all'", 
            "'keys'", "'hash'", "'choose'", "'end'", "'and='", "'or='", 
            "'=>='", "'&='", "'|='", "'^='", "'-='", "'+='", "'*='", "'/='", 
            "'//='", "'%='", "'mod='", "'**='", "'>>='", "'#'", "'(*'", 
            "'*)'", "'!'", "'*'", "'as'", "'.'", "'import'", "'print'", 
            "'from'", "'..'", "'setintlevel'", "'->'", "'stop'", "'lambda'", 
            "'?'", "'not'", "','", "'const'", "'await'", "'assert'", "'var'", 
            "'trap'", "'possibly'", "'pass'", "'del'", "'spawn'", "'invariant'", 
            "'go'", "'sequential'", "'when'", "'let'", "'if'", "'elif'", 
            "'else'", "'@'", "'while'", "'def'", "'exists'", "'where'", 
            "'='", "'for'", "'in'", "':'", "'None'", "'atomically'", "'eternal'", 
            "'['", "']'", "'{'", "'}'", "'('", "')'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "NL", "WS", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
            "POINTER_OF", "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", 
            "RANGE", "SETINTLEVEL", "ARROW", "STOP", "LAMBDA", "ADDRESS_OF", 
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
                  "T__50", "T__51", "T__52", "T__53", "NL", "WS", "COMMENT", 
                  "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
                  "POINTER_OF", "STAR", "AS", "DOT", "IMPORT", "PRINT", 
                  "FROM", "RANGE", "SETINTLEVEL", "ARROW", "STOP", "LAMBDA", 
                  "ADDRESS_OF", "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", 
                  "VAR", "TRAP", "POSSIBLY", "PASS", "DEL", "SPAWN", "INVARIANT", 
                  "GO", "SEQUENTIAL", "WHEN", "LET", "IF", "ELIF", "ELSE", 
                  "AT", "WHILE", "DEF", "EXISTS", "WHERE", "EQ", "FOR", 
                  "IN", "COLON", "NONE", "ATOMICALLY", "BOOL", "ETERNAL", 
                  "INT", "NAME", "ATOM", "HEX_INTEGER", "HEX_DIGIT", "OPEN_BRACK", 
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


    class HarmonyDenter(ModifiedDenterHelper):
        def __init__(self, lexer, nl_token, colon_token, indent_token, dedent_token, ignore_eof):
            super().__init__(lexer, nl_token, colon_token, indent_token, dedent_token, ignore_eof)
            self.lexer: HarmonyLexer = lexer

        def pull_token(self):
            return super(HarmonyLexer, self.lexer).nextToken()

    @property
    def opened_for(self):
        try:
            return self._opened_for
        except AttributeError:
            self._opened_for = 0
            return self._opened_for

    @opened_for.setter
    def opened_for(self, value):
        self._opened_for = value

    @property
    def opened(self):
        try:
            return self._opened
        except AttributeError:
            self._opened = 0
            return self._opened

    @opened.setter
    def opened(self, value):
        self._opened = value

    denter = None

    def nextToken(self):
        if not self.denter:
            self.denter = self.HarmonyDenter(self, self.NL, self.COLON, HarmonyParser.INDENT, HarmonyParser.DEDENT, ignore_eof=False)
        token = self.denter.next_token()
        return token


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[54] = self.NL_action 
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
     


