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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2w")
        buf.write("\u037b\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("y\ty\4z\tz\4{\t{\4|\t|\4}\t}\3\2\3\2\3\2\3\2\3\3\3\3\3")
        buf.write("\3\3\4\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t")
        buf.write("\3\n\3\n\3\n\3\13\3\13\3\f\3\f\3\r\3\r\3\r\3\r\3\16\3")
        buf.write("\16\3\16\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\22\3\22\3\22\3\23\3\23\3\24\3\24\3\24\3\25\3\25\3\26")
        buf.write("\3\26\3\26\3\27\3\27\3\30\3\30\3\30\3\30\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\33\3\33")
        buf.write("\3\33\3\33\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3 \3 \3")
        buf.write(" \3 \3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3#\3#\3#\3#\3$\3$")
        buf.write("\3$\3$\3%\3%\3%\3%\3%\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3")
        buf.write("\'\3\'\3\'\3(\3(\3(\3(\3)\3)\3)\3)\3)\3*\3*\3*\3*\3+\3")
        buf.write("+\3+\3+\3,\3,\3,\3-\3-\3-\3.\3.\3.\3/\3/\3/\3\60\3\60")
        buf.write("\3\60\3\61\3\61\3\61\3\62\3\62\3\62\3\63\3\63\3\63\3\63")
        buf.write("\3\64\3\64\3\64\3\65\3\65\3\65\3\65\3\65\3\66\3\66\3\66")
        buf.write("\3\66\3\67\3\67\3\67\3\67\38\58\u01d3\n8\38\38\78\u01d7")
        buf.write("\n8\f8\168\u01da\138\38\78\u01dd\n8\f8\168\u01e0\138\5")
        buf.write("8\u01e2\n8\38\38\39\69\u01e7\n9\r9\169\u01e8\39\69\u01ec")
        buf.write("\n9\r9\169\u01ed\39\39\39\59\u01f3\n9\39\39\3:\3:\7:\u01f9")
        buf.write("\n:\f:\16:\u01fc\13:\3:\3:\3:\3:\7:\u0202\n:\f:\16:\u0205")
        buf.write("\13:\5:\u0207\n:\3;\3;\3<\3<\3<\3=\3=\3=\3>\3>\3?\3?\3")
        buf.write("@\3@\3@\3A\3A\3B\3B\3B\3B\3B\3B\3B\3C\3C\3C\3C\3C\3C\3")
        buf.write("D\3D\3D\3D\3D\3E\3E\3E\3F\3F\3F\3F\3F\3F\3F\3F\3F\3F\3")
        buf.write("F\3F\3G\3G\3G\3H\3H\3H\3H\3H\3I\3I\3I\3I\3I\3J\3J\3J\3")
        buf.write("J\3J\3J\3J\3K\3K\3L\3L\3L\3L\3M\3M\3N\3N\3N\3N\3N\3N\3")
        buf.write("O\3O\3O\3O\3O\3O\3P\3P\3P\3P\3P\3P\3P\3Q\3Q\3Q\3Q\3R\3")
        buf.write("R\3R\3R\3R\3S\3S\3S\3S\3S\3T\3T\3T\3T\3U\3U\3U\3U\3U\3")
        buf.write("U\3V\3V\3V\3V\3V\3V\3V\3V\3V\3V\3W\3W\3W\3X\3X\3X\3X\3")
        buf.write("X\3X\3X\3X\3X\3X\3X\3Y\3Y\3Y\3Y\3Y\3Z\3Z\3Z\3Z\3[\3[\3")
        buf.write("[\3\\\3\\\3\\\3\\\3\\\3]\3]\3]\3]\3]\3^\3^\3_\3_\3_\3")
        buf.write("_\3_\3_\3`\3`\3`\3`\3a\3a\3a\3a\3a\3a\3a\3b\3b\3b\3b\3")
        buf.write("b\3b\3c\3c\3d\3d\3d\3d\3d\3d\3e\3e\3e\3e\3e\3f\3f\3g\3")
        buf.write("g\3g\3g\3g\3h\3h\3h\3h\3h\3h\3h\3h\3h\3h\3h\3i\3i\3i\3")
        buf.write("i\3i\3i\3i\3i\3i\5i\u02f1\ni\3j\3j\3j\3j\3j\3j\3j\3j\3")
        buf.write("k\3k\3k\3k\3k\3k\3k\3k\3k\3k\3k\3k\3k\3l\6l\u0309\nl\r")
        buf.write("l\16l\u030a\3l\3l\3l\5l\u0310\nl\3m\3m\7m\u0314\nm\fm")
        buf.write("\16m\u0317\13m\3n\3n\3n\5n\u031c\nn\3o\3o\3o\3o\6o\u0322")
        buf.write("\no\ro\16o\u0323\3p\3p\3q\3q\3q\3r\3r\3r\3s\3s\3s\3t\3")
        buf.write("t\3t\3u\3u\3u\3v\3v\3v\3w\3w\3x\3x\5x\u033e\nx\3y\3y\3")
        buf.write("y\7y\u0343\ny\fy\16y\u0346\13y\3y\3y\3y\3y\7y\u034c\n")
        buf.write("y\fy\16y\u034f\13y\3y\5y\u0352\ny\3z\3z\3z\3z\3z\7z\u0359")
        buf.write("\nz\fz\16z\u035c\13z\3z\3z\3z\3z\3z\3z\3z\3z\7z\u0366")
        buf.write("\nz\fz\16z\u0369\13z\3z\3z\3z\5z\u036e\nz\3{\3{\5{\u0372")
        buf.write("\n{\3|\3|\3}\3}\3}\3}\5}\u037a\n}\5\u01fa\u035a\u0367")
        buf.write("\2~\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r")
        buf.write("\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30")
        buf.write("/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'")
        buf.write("M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q")
        buf.write(":s\2u;w<y={>}?\177@\u0081A\u0083B\u0085C\u0087D\u0089")
        buf.write("E\u008bF\u008dG\u008fH\u0091I\u0093J\u0095K\u0097L\u0099")
        buf.write("M\u009bN\u009dO\u009fP\u00a1Q\u00a3R\u00a5S\u00a7T\u00a9")
        buf.write("U\u00abV\u00adW\u00afX\u00b1Y\u00b3Z\u00b5[\u00b7\\\u00b9")
        buf.write("]\u00bb^\u00bd_\u00bf`\u00c1a\u00c3b\u00c5c\u00c7d\u00c9")
        buf.write("e\u00cbf\u00cdg\u00cfh\u00d1i\u00d3j\u00d5k\u00d7l\u00d9")
        buf.write("m\u00dbn\u00ddo\u00df\2\u00e1p\u00e3q\u00e5r\u00e7s\u00e9")
        buf.write("t\u00ebu\u00edv\u00efw\u00f1\2\u00f3\2\u00f5\2\u00f7\2")
        buf.write("\u00f9\2\3\2\13\4\2\f\f\16\17\3\2\62;\5\2C\\aac|\6\2\62")
        buf.write(";C\\aac|\3\2\60\60\5\2\62;CHch\6\2\f\f\16\17))^^\6\2\f")
        buf.write("\f\16\17$$^^\3\2^^\2\u0390\2\3\3\2\2\2\2\5\3\2\2\2\2\7")
        buf.write("\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2")
        buf.write("\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2")
        buf.write("\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2")
        buf.write("\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2")
        buf.write("\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63")
        buf.write("\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2")
        buf.write("\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2")
        buf.write("\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3")
        buf.write("\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y")
        buf.write("\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2")
        buf.write("c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2")
        buf.write("\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2u\3\2\2\2\2w\3\2\2")
        buf.write("\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081")
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
        buf.write("\2\2\u00dd\3\2\2\2\2\u00e1\3\2\2\2\2\u00e3\3\2\2\2\2\u00e5")
        buf.write("\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9\3\2\2\2\2\u00eb\3\2\2")
        buf.write("\2\2\u00ed\3\2\2\2\2\u00ef\3\2\2\2\3\u00fb\3\2\2\2\5\u00ff")
        buf.write("\3\2\2\2\7\u0102\3\2\2\2\t\u0105\3\2\2\2\13\u0107\3\2")
        buf.write("\2\2\r\u0109\3\2\2\2\17\u010b\3\2\2\2\21\u010d\3\2\2\2")
        buf.write("\23\u010f\3\2\2\2\25\u0112\3\2\2\2\27\u0114\3\2\2\2\31")
        buf.write("\u0116\3\2\2\2\33\u011a\3\2\2\2\35\u011d\3\2\2\2\37\u0120")
        buf.write("\3\2\2\2!\u0123\3\2\2\2#\u0126\3\2\2\2%\u0129\3\2\2\2")
        buf.write("\'\u012b\3\2\2\2)\u012e\3\2\2\2+\u0130\3\2\2\2-\u0133")
        buf.write("\3\2\2\2/\u0135\3\2\2\2\61\u0139\3\2\2\2\63\u0141\3\2")
        buf.write("\2\2\65\u014c\3\2\2\2\67\u0158\3\2\2\29\u0161\3\2\2\2")
        buf.write(";\u0169\3\2\2\2=\u016d\3\2\2\2?\u0171\3\2\2\2A\u0175\3")
        buf.write("\2\2\2C\u017a\3\2\2\2E\u017e\3\2\2\2G\u0182\3\2\2\2I\u0186")
        buf.write("\3\2\2\2K\u018b\3\2\2\2M\u0190\3\2\2\2O\u0197\3\2\2\2")
        buf.write("Q\u019b\3\2\2\2S\u01a0\3\2\2\2U\u01a4\3\2\2\2W\u01a8\3")
        buf.write("\2\2\2Y\u01ab\3\2\2\2[\u01ae\3\2\2\2]\u01b1\3\2\2\2_\u01b4")
        buf.write("\3\2\2\2a\u01b7\3\2\2\2c\u01ba\3\2\2\2e\u01bd\3\2\2\2")
        buf.write("g\u01c1\3\2\2\2i\u01c4\3\2\2\2k\u01c9\3\2\2\2m\u01cd\3")
        buf.write("\2\2\2o\u01d2\3\2\2\2q\u01f2\3\2\2\2s\u0206\3\2\2\2u\u0208")
        buf.write("\3\2\2\2w\u020a\3\2\2\2y\u020d\3\2\2\2{\u0210\3\2\2\2")
        buf.write("}\u0212\3\2\2\2\177\u0214\3\2\2\2\u0081\u0217\3\2\2\2")
        buf.write("\u0083\u0219\3\2\2\2\u0085\u0220\3\2\2\2\u0087\u0226\3")
        buf.write("\2\2\2\u0089\u022b\3\2\2\2\u008b\u022e\3\2\2\2\u008d\u023a")
        buf.write("\3\2\2\2\u008f\u023d\3\2\2\2\u0091\u0242\3\2\2\2\u0093")
        buf.write("\u0247\3\2\2\2\u0095\u024e\3\2\2\2\u0097\u0250\3\2\2\2")
        buf.write("\u0099\u0254\3\2\2\2\u009b\u0256\3\2\2\2\u009d\u025c\3")
        buf.write("\2\2\2\u009f\u0262\3\2\2\2\u00a1\u0269\3\2\2\2\u00a3\u026d")
        buf.write("\3\2\2\2\u00a5\u0272\3\2\2\2\u00a7\u0277\3\2\2\2\u00a9")
        buf.write("\u027b\3\2\2\2\u00ab\u0281\3\2\2\2\u00ad\u028b\3\2\2\2")
        buf.write("\u00af\u028e\3\2\2\2\u00b1\u0299\3\2\2\2\u00b3\u029e\3")
        buf.write("\2\2\2\u00b5\u02a2\3\2\2\2\u00b7\u02a5\3\2\2\2\u00b9\u02aa")
        buf.write("\3\2\2\2\u00bb\u02af\3\2\2\2\u00bd\u02b1\3\2\2\2\u00bf")
        buf.write("\u02b7\3\2\2\2\u00c1\u02bb\3\2\2\2\u00c3\u02c2\3\2\2\2")
        buf.write("\u00c5\u02c8\3\2\2\2\u00c7\u02ca\3\2\2\2\u00c9\u02d0\3")
        buf.write("\2\2\2\u00cb\u02d5\3\2\2\2\u00cd\u02d7\3\2\2\2\u00cf\u02dc")
        buf.write("\3\2\2\2\u00d1\u02f0\3\2\2\2\u00d3\u02f2\3\2\2\2\u00d5")
        buf.write("\u02fa\3\2\2\2\u00d7\u030f\3\2\2\2\u00d9\u0311\3\2\2\2")
        buf.write("\u00db\u0318\3\2\2\2\u00dd\u031d\3\2\2\2\u00df\u0325\3")
        buf.write("\2\2\2\u00e1\u0327\3\2\2\2\u00e3\u032a\3\2\2\2\u00e5\u032d")
        buf.write("\3\2\2\2\u00e7\u0330\3\2\2\2\u00e9\u0333\3\2\2\2\u00eb")
        buf.write("\u0336\3\2\2\2\u00ed\u0339\3\2\2\2\u00ef\u033d\3\2\2\2")
        buf.write("\u00f1\u0351\3\2\2\2\u00f3\u036d\3\2\2\2\u00f5\u0371\3")
        buf.write("\2\2\2\u00f7\u0373\3\2\2\2\u00f9\u0379\3\2\2\2\u00fb\u00fc")
        buf.write("\7c\2\2\u00fc\u00fd\7p\2\2\u00fd\u00fe\7f\2\2\u00fe\4")
        buf.write("\3\2\2\2\u00ff\u0100\7q\2\2\u0100\u0101\7t\2\2\u0101\6")
        buf.write("\3\2\2\2\u0102\u0103\7?\2\2\u0103\u0104\7@\2\2\u0104\b")
        buf.write("\3\2\2\2\u0105\u0106\7(\2\2\u0106\n\3\2\2\2\u0107\u0108")
        buf.write("\7~\2\2\u0108\f\3\2\2\2\u0109\u010a\7`\2\2\u010a\16\3")
        buf.write("\2\2\2\u010b\u010c\7/\2\2\u010c\20\3\2\2\2\u010d\u010e")
        buf.write("\7-\2\2\u010e\22\3\2\2\2\u010f\u0110\7\61\2\2\u0110\u0111")
        buf.write("\7\61\2\2\u0111\24\3\2\2\2\u0112\u0113\7\61\2\2\u0113")
        buf.write("\26\3\2\2\2\u0114\u0115\7\'\2\2\u0115\30\3\2\2\2\u0116")
        buf.write("\u0117\7o\2\2\u0117\u0118\7q\2\2\u0118\u0119\7f\2\2\u0119")
        buf.write("\32\3\2\2\2\u011a\u011b\7,\2\2\u011b\u011c\7,\2\2\u011c")
        buf.write("\34\3\2\2\2\u011d\u011e\7>\2\2\u011e\u011f\7>\2\2\u011f")
        buf.write("\36\3\2\2\2\u0120\u0121\7@\2\2\u0121\u0122\7@\2\2\u0122")
        buf.write(" \3\2\2\2\u0123\u0124\7?\2\2\u0124\u0125\7?\2\2\u0125")
        buf.write("\"\3\2\2\2\u0126\u0127\7#\2\2\u0127\u0128\7?\2\2\u0128")
        buf.write("$\3\2\2\2\u0129\u012a\7>\2\2\u012a&\3\2\2\2\u012b\u012c")
        buf.write("\7>\2\2\u012c\u012d\7?\2\2\u012d(\3\2\2\2\u012e\u012f")
        buf.write("\7@\2\2\u012f*\3\2\2\2\u0130\u0131\7@\2\2\u0131\u0132")
        buf.write("\7?\2\2\u0132,\3\2\2\2\u0133\u0134\7\u0080\2\2\u0134.")
        buf.write("\3\2\2\2\u0135\u0136\7c\2\2\u0136\u0137\7d\2\2\u0137\u0138")
        buf.write("\7u\2\2\u0138\60\3\2\2\2\u0139\u013a\7c\2\2\u013a\u013b")
        buf.write("\7v\2\2\u013b\u013c\7N\2\2\u013c\u013d\7c\2\2\u013d\u013e")
        buf.write("\7d\2\2\u013e\u013f\7g\2\2\u013f\u0140\7n\2\2\u0140\62")
        buf.write("\3\2\2\2\u0141\u0142\7e\2\2\u0142\u0143\7q\2\2\u0143\u0144")
        buf.write("\7w\2\2\u0144\u0145\7p\2\2\u0145\u0146\7v\2\2\u0146\u0147")
        buf.write("\7N\2\2\u0147\u0148\7c\2\2\u0148\u0149\7d\2\2\u0149\u014a")
        buf.write("\7g\2\2\u014a\u014b\7n\2\2\u014b\64\3\2\2\2\u014c\u014d")
        buf.write("\7i\2\2\u014d\u014e\7g\2\2\u014e\u014f\7v\2\2\u014f\u0150")
        buf.write("\7a\2\2\u0150\u0151\7e\2\2\u0151\u0152\7q\2\2\u0152\u0153")
        buf.write("\7p\2\2\u0153\u0154\7v\2\2\u0154\u0155\7g\2\2\u0155\u0156")
        buf.write("\7z\2\2\u0156\u0157\7v\2\2\u0157\66\3\2\2\2\u0158\u0159")
        buf.write("\7e\2\2\u0159\u015a\7q\2\2\u015a\u015b\7p\2\2\u015b\u015c")
        buf.write("\7v\2\2\u015c\u015d\7g\2\2\u015d\u015e\7z\2\2\u015e\u015f")
        buf.write("\7v\2\2\u015f\u0160\7u\2\2\u01608\3\2\2\2\u0161\u0162")
        buf.write("\7k\2\2\u0162\u0163\7u\2\2\u0163\u0164\7G\2\2\u0164\u0165")
        buf.write("\7o\2\2\u0165\u0166\7r\2\2\u0166\u0167\7v\2\2\u0167\u0168")
        buf.write("\7{\2\2\u0168:\3\2\2\2\u0169\u016a\7o\2\2\u016a\u016b")
        buf.write("\7k\2\2\u016b\u016c\7p\2\2\u016c<\3\2\2\2\u016d\u016e")
        buf.write("\7o\2\2\u016e\u016f\7c\2\2\u016f\u0170\7z\2\2\u0170>\3")
        buf.write("\2\2\2\u0171\u0172\7n\2\2\u0172\u0173\7g\2\2\u0173\u0174")
        buf.write("\7p\2\2\u0174@\3\2\2\2\u0175\u0176\7v\2\2\u0176\u0177")
        buf.write("\7{\2\2\u0177\u0178\7r\2\2\u0178\u0179\7g\2\2\u0179B\3")
        buf.write("\2\2\2\u017a\u017b\7u\2\2\u017b\u017c\7v\2\2\u017c\u017d")
        buf.write("\7t\2\2\u017dD\3\2\2\2\u017e\u017f\7c\2\2\u017f\u0180")
        buf.write("\7p\2\2\u0180\u0181\7{\2\2\u0181F\3\2\2\2\u0182\u0183")
        buf.write("\7c\2\2\u0183\u0184\7n\2\2\u0184\u0185\7n\2\2\u0185H\3")
        buf.write("\2\2\2\u0186\u0187\7m\2\2\u0187\u0188\7g\2\2\u0188\u0189")
        buf.write("\7{\2\2\u0189\u018a\7u\2\2\u018aJ\3\2\2\2\u018b\u018c")
        buf.write("\7j\2\2\u018c\u018d\7c\2\2\u018d\u018e\7u\2\2\u018e\u018f")
        buf.write("\7j\2\2\u018fL\3\2\2\2\u0190\u0191\7e\2\2\u0191\u0192")
        buf.write("\7j\2\2\u0192\u0193\7q\2\2\u0193\u0194\7q\2\2\u0194\u0195")
        buf.write("\7u\2\2\u0195\u0196\7g\2\2\u0196N\3\2\2\2\u0197\u0198")
        buf.write("\7g\2\2\u0198\u0199\7p\2\2\u0199\u019a\7f\2\2\u019aP\3")
        buf.write("\2\2\2\u019b\u019c\7c\2\2\u019c\u019d\7p\2\2\u019d\u019e")
        buf.write("\7f\2\2\u019e\u019f\7?\2\2\u019fR\3\2\2\2\u01a0\u01a1")
        buf.write("\7q\2\2\u01a1\u01a2\7t\2\2\u01a2\u01a3\7?\2\2\u01a3T\3")
        buf.write("\2\2\2\u01a4\u01a5\7?\2\2\u01a5\u01a6\7@\2\2\u01a6\u01a7")
        buf.write("\7?\2\2\u01a7V\3\2\2\2\u01a8\u01a9\7(\2\2\u01a9\u01aa")
        buf.write("\7?\2\2\u01aaX\3\2\2\2\u01ab\u01ac\7~\2\2\u01ac\u01ad")
        buf.write("\7?\2\2\u01adZ\3\2\2\2\u01ae\u01af\7`\2\2\u01af\u01b0")
        buf.write("\7?\2\2\u01b0\\\3\2\2\2\u01b1\u01b2\7/\2\2\u01b2\u01b3")
        buf.write("\7?\2\2\u01b3^\3\2\2\2\u01b4\u01b5\7-\2\2\u01b5\u01b6")
        buf.write("\7?\2\2\u01b6`\3\2\2\2\u01b7\u01b8\7,\2\2\u01b8\u01b9")
        buf.write("\7?\2\2\u01b9b\3\2\2\2\u01ba\u01bb\7\61\2\2\u01bb\u01bc")
        buf.write("\7?\2\2\u01bcd\3\2\2\2\u01bd\u01be\7\61\2\2\u01be\u01bf")
        buf.write("\7\61\2\2\u01bf\u01c0\7?\2\2\u01c0f\3\2\2\2\u01c1\u01c2")
        buf.write("\7\'\2\2\u01c2\u01c3\7?\2\2\u01c3h\3\2\2\2\u01c4\u01c5")
        buf.write("\7o\2\2\u01c5\u01c6\7q\2\2\u01c6\u01c7\7f\2\2\u01c7\u01c8")
        buf.write("\7?\2\2\u01c8j\3\2\2\2\u01c9\u01ca\7,\2\2\u01ca\u01cb")
        buf.write("\7,\2\2\u01cb\u01cc\7?\2\2\u01ccl\3\2\2\2\u01cd\u01ce")
        buf.write("\7@\2\2\u01ce\u01cf\7@\2\2\u01cf\u01d0\7?\2\2\u01d0n\3")
        buf.write("\2\2\2\u01d1\u01d3\7\17\2\2\u01d2\u01d1\3\2\2\2\u01d2")
        buf.write("\u01d3\3\2\2\2\u01d3\u01d4\3\2\2\2\u01d4\u01e1\7\f\2\2")
        buf.write("\u01d5\u01d7\7\"\2\2\u01d6\u01d5\3\2\2\2\u01d7\u01da\3")
        buf.write("\2\2\2\u01d8\u01d6\3\2\2\2\u01d8\u01d9\3\2\2\2\u01d9\u01e2")
        buf.write("\3\2\2\2\u01da\u01d8\3\2\2\2\u01db\u01dd\7\13\2\2\u01dc")
        buf.write("\u01db\3\2\2\2\u01dd\u01e0\3\2\2\2\u01de\u01dc\3\2\2\2")
        buf.write("\u01de\u01df\3\2\2\2\u01df\u01e2\3\2\2\2\u01e0\u01de\3")
        buf.write("\2\2\2\u01e1\u01d8\3\2\2\2\u01e1\u01de\3\2\2\2\u01e2\u01e3")
        buf.write("\3\2\2\2\u01e3\u01e4\b8\2\2\u01e4p\3\2\2\2\u01e5\u01e7")
        buf.write("\7\"\2\2\u01e6\u01e5\3\2\2\2\u01e7\u01e8\3\2\2\2\u01e8")
        buf.write("\u01e6\3\2\2\2\u01e8\u01e9\3\2\2\2\u01e9\u01f3\3\2\2\2")
        buf.write("\u01ea\u01ec\7\13\2\2\u01eb\u01ea\3\2\2\2\u01ec\u01ed")
        buf.write("\3\2\2\2\u01ed\u01eb\3\2\2\2\u01ed\u01ee\3\2\2\2\u01ee")
        buf.write("\u01f3\3\2\2\2\u01ef\u01f0\7^\2\2\u01f0\u01f3\5o8\2\u01f1")
        buf.write("\u01f3\5s:\2\u01f2\u01e6\3\2\2\2\u01f2\u01eb\3\2\2\2\u01f2")
        buf.write("\u01ef\3\2\2\2\u01f2\u01f1\3\2\2\2\u01f3\u01f4\3\2\2\2")
        buf.write("\u01f4\u01f5\b9\3\2\u01f5r\3\2\2\2\u01f6\u01fa\5w<\2\u01f7")
        buf.write("\u01f9\13\2\2\2\u01f8\u01f7\3\2\2\2\u01f9\u01fc\3\2\2")
        buf.write("\2\u01fa\u01fb\3\2\2\2\u01fa\u01f8\3\2\2\2\u01fb\u01fd")
        buf.write("\3\2\2\2\u01fc\u01fa\3\2\2\2\u01fd\u01fe\5y=\2\u01fe\u0207")
        buf.write("\3\2\2\2\u01ff\u0203\5u;\2\u0200\u0202\n\2\2\2\u0201\u0200")
        buf.write("\3\2\2\2\u0202\u0205\3\2\2\2\u0203\u0201\3\2\2\2\u0203")
        buf.write("\u0204\3\2\2\2\u0204\u0207\3\2\2\2\u0205\u0203\3\2\2\2")
        buf.write("\u0206\u01f6\3\2\2\2\u0206\u01ff\3\2\2\2\u0207t\3\2\2")
        buf.write("\2\u0208\u0209\7%\2\2\u0209v\3\2\2\2\u020a\u020b\7*\2")
        buf.write("\2\u020b\u020c\7,\2\2\u020cx\3\2\2\2\u020d\u020e\7,\2")
        buf.write("\2\u020e\u020f\7+\2\2\u020fz\3\2\2\2\u0210\u0211\7#\2")
        buf.write("\2\u0211|\3\2\2\2\u0212\u0213\7,\2\2\u0213~\3\2\2\2\u0214")
        buf.write("\u0215\7c\2\2\u0215\u0216\7u\2\2\u0216\u0080\3\2\2\2\u0217")
        buf.write("\u0218\7\60\2\2\u0218\u0082\3\2\2\2\u0219\u021a\7k\2\2")
        buf.write("\u021a\u021b\7o\2\2\u021b\u021c\7r\2\2\u021c\u021d\7q")
        buf.write("\2\2\u021d\u021e\7t\2\2\u021e\u021f\7v\2\2\u021f\u0084")
        buf.write("\3\2\2\2\u0220\u0221\7r\2\2\u0221\u0222\7t\2\2\u0222\u0223")
        buf.write("\7k\2\2\u0223\u0224\7p\2\2\u0224\u0225\7v\2\2\u0225\u0086")
        buf.write("\3\2\2\2\u0226\u0227\7h\2\2\u0227\u0228\7t\2\2\u0228\u0229")
        buf.write("\7q\2\2\u0229\u022a\7o\2\2\u022a\u0088\3\2\2\2\u022b\u022c")
        buf.write("\7\60\2\2\u022c\u022d\7\60\2\2\u022d\u008a\3\2\2\2\u022e")
        buf.write("\u022f\7u\2\2\u022f\u0230\7g\2\2\u0230\u0231\7v\2\2\u0231")
        buf.write("\u0232\7k\2\2\u0232\u0233\7p\2\2\u0233\u0234\7v\2\2\u0234")
        buf.write("\u0235\7n\2\2\u0235\u0236\7g\2\2\u0236\u0237\7x\2\2\u0237")
        buf.write("\u0238\7g\2\2\u0238\u0239\7n\2\2\u0239\u008c\3\2\2\2\u023a")
        buf.write("\u023b\7/\2\2\u023b\u023c\7@\2\2\u023c\u008e\3\2\2\2\u023d")
        buf.write("\u023e\7u\2\2\u023e\u023f\7c\2\2\u023f\u0240\7x\2\2\u0240")
        buf.write("\u0241\7g\2\2\u0241\u0090\3\2\2\2\u0242\u0243\7u\2\2\u0243")
        buf.write("\u0244\7v\2\2\u0244\u0245\7q\2\2\u0245\u0246\7r\2\2\u0246")
        buf.write("\u0092\3\2\2\2\u0247\u0248\7n\2\2\u0248\u0249\7c\2\2\u0249")
        buf.write("\u024a\7o\2\2\u024a\u024b\7d\2\2\u024b\u024c\7f\2\2\u024c")
        buf.write("\u024d\7c\2\2\u024d\u0094\3\2\2\2\u024e\u024f\7A\2\2\u024f")
        buf.write("\u0096\3\2\2\2\u0250\u0251\7p\2\2\u0251\u0252\7q\2\2\u0252")
        buf.write("\u0253\7v\2\2\u0253\u0098\3\2\2\2\u0254\u0255\7.\2\2\u0255")
        buf.write("\u009a\3\2\2\2\u0256\u0257\7e\2\2\u0257\u0258\7q\2\2\u0258")
        buf.write("\u0259\7p\2\2\u0259\u025a\7u\2\2\u025a\u025b\7v\2\2\u025b")
        buf.write("\u009c\3\2\2\2\u025c\u025d\7c\2\2\u025d\u025e\7y\2\2\u025e")
        buf.write("\u025f\7c\2\2\u025f\u0260\7k\2\2\u0260\u0261\7v\2\2\u0261")
        buf.write("\u009e\3\2\2\2\u0262\u0263\7c\2\2\u0263\u0264\7u\2\2\u0264")
        buf.write("\u0265\7u\2\2\u0265\u0266\7g\2\2\u0266\u0267\7t\2\2\u0267")
        buf.write("\u0268\7v\2\2\u0268\u00a0\3\2\2\2\u0269\u026a\7x\2\2\u026a")
        buf.write("\u026b\7c\2\2\u026b\u026c\7t\2\2\u026c\u00a2\3\2\2\2\u026d")
        buf.write("\u026e\7v\2\2\u026e\u026f\7t\2\2\u026f\u0270\7c\2\2\u0270")
        buf.write("\u0271\7r\2\2\u0271\u00a4\3\2\2\2\u0272\u0273\7r\2\2\u0273")
        buf.write("\u0274\7c\2\2\u0274\u0275\7u\2\2\u0275\u0276\7u\2\2\u0276")
        buf.write("\u00a6\3\2\2\2\u0277\u0278\7f\2\2\u0278\u0279\7g\2\2\u0279")
        buf.write("\u027a\7n\2\2\u027a\u00a8\3\2\2\2\u027b\u027c\7u\2\2\u027c")
        buf.write("\u027d\7r\2\2\u027d\u027e\7c\2\2\u027e\u027f\7y\2\2\u027f")
        buf.write("\u0280\7p\2\2\u0280\u00aa\3\2\2\2\u0281\u0282\7k\2\2\u0282")
        buf.write("\u0283\7p\2\2\u0283\u0284\7x\2\2\u0284\u0285\7c\2\2\u0285")
        buf.write("\u0286\7t\2\2\u0286\u0287\7k\2\2\u0287\u0288\7c\2\2\u0288")
        buf.write("\u0289\7p\2\2\u0289\u028a\7v\2\2\u028a\u00ac\3\2\2\2\u028b")
        buf.write("\u028c\7i\2\2\u028c\u028d\7q\2\2\u028d\u00ae\3\2\2\2\u028e")
        buf.write("\u028f\7u\2\2\u028f\u0290\7g\2\2\u0290\u0291\7s\2\2\u0291")
        buf.write("\u0292\7w\2\2\u0292\u0293\7g\2\2\u0293\u0294\7p\2\2\u0294")
        buf.write("\u0295\7v\2\2\u0295\u0296\7k\2\2\u0296\u0297\7c\2\2\u0297")
        buf.write("\u0298\7n\2\2\u0298\u00b0\3\2\2\2\u0299\u029a\7y\2\2\u029a")
        buf.write("\u029b\7j\2\2\u029b\u029c\7g\2\2\u029c\u029d\7p\2\2\u029d")
        buf.write("\u00b2\3\2\2\2\u029e\u029f\7n\2\2\u029f\u02a0\7g\2\2\u02a0")
        buf.write("\u02a1\7v\2\2\u02a1\u00b4\3\2\2\2\u02a2\u02a3\7k\2\2\u02a3")
        buf.write("\u02a4\7h\2\2\u02a4\u00b6\3\2\2\2\u02a5\u02a6\7g\2\2\u02a6")
        buf.write("\u02a7\7n\2\2\u02a7\u02a8\7k\2\2\u02a8\u02a9\7h\2\2\u02a9")
        buf.write("\u00b8\3\2\2\2\u02aa\u02ab\7g\2\2\u02ab\u02ac\7n\2\2\u02ac")
        buf.write("\u02ad\7u\2\2\u02ad\u02ae\7g\2\2\u02ae\u00ba\3\2\2\2\u02af")
        buf.write("\u02b0\7B\2\2\u02b0\u00bc\3\2\2\2\u02b1\u02b2\7y\2\2\u02b2")
        buf.write("\u02b3\7j\2\2\u02b3\u02b4\7k\2\2\u02b4\u02b5\7n\2\2\u02b5")
        buf.write("\u02b6\7g\2\2\u02b6\u00be\3\2\2\2\u02b7\u02b8\7f\2\2\u02b8")
        buf.write("\u02b9\7g\2\2\u02b9\u02ba\7h\2\2\u02ba\u00c0\3\2\2\2\u02bb")
        buf.write("\u02bc\7g\2\2\u02bc\u02bd\7z\2\2\u02bd\u02be\7k\2\2\u02be")
        buf.write("\u02bf\7u\2\2\u02bf\u02c0\7v\2\2\u02c0\u02c1\7u\2\2\u02c1")
        buf.write("\u00c2\3\2\2\2\u02c2\u02c3\7y\2\2\u02c3\u02c4\7j\2\2\u02c4")
        buf.write("\u02c5\7g\2\2\u02c5\u02c6\7t\2\2\u02c6\u02c7\7g\2\2\u02c7")
        buf.write("\u00c4\3\2\2\2\u02c8\u02c9\7?\2\2\u02c9\u00c6\3\2\2\2")
        buf.write("\u02ca\u02cb\7h\2\2\u02cb\u02cc\7q\2\2\u02cc\u02cd\7t")
        buf.write("\2\2\u02cd\u02ce\3\2\2\2\u02ce\u02cf\bd\4\2\u02cf\u00c8")
        buf.write("\3\2\2\2\u02d0\u02d1\7k\2\2\u02d1\u02d2\7p\2\2\u02d2\u02d3")
        buf.write("\3\2\2\2\u02d3\u02d4\be\5\2\u02d4\u00ca\3\2\2\2\u02d5")
        buf.write("\u02d6\7<\2\2\u02d6\u00cc\3\2\2\2\u02d7\u02d8\7P\2\2\u02d8")
        buf.write("\u02d9\7q\2\2\u02d9\u02da\7p\2\2\u02da\u02db\7g\2\2\u02db")
        buf.write("\u00ce\3\2\2\2\u02dc\u02dd\7c\2\2\u02dd\u02de\7v\2\2\u02de")
        buf.write("\u02df\7q\2\2\u02df\u02e0\7o\2\2\u02e0\u02e1\7k\2\2\u02e1")
        buf.write("\u02e2\7e\2\2\u02e2\u02e3\7c\2\2\u02e3\u02e4\7n\2\2\u02e4")
        buf.write("\u02e5\7n\2\2\u02e5\u02e6\7{\2\2\u02e6\u00d0\3\2\2\2\u02e7")
        buf.write("\u02e8\7H\2\2\u02e8\u02e9\7c\2\2\u02e9\u02ea\7n\2\2\u02ea")
        buf.write("\u02eb\7u\2\2\u02eb\u02f1\7g\2\2\u02ec\u02ed\7V\2\2\u02ed")
        buf.write("\u02ee\7t\2\2\u02ee\u02ef\7w\2\2\u02ef\u02f1\7g\2\2\u02f0")
        buf.write("\u02e7\3\2\2\2\u02f0\u02ec\3\2\2\2\u02f1\u00d2\3\2\2\2")
        buf.write("\u02f2\u02f3\7g\2\2\u02f3\u02f4\7v\2\2\u02f4\u02f5\7g")
        buf.write("\2\2\u02f5\u02f6\7t\2\2\u02f6\u02f7\7p\2\2\u02f7\u02f8")
        buf.write("\7c\2\2\u02f8\u02f9\7n\2\2\u02f9\u00d4\3\2\2\2\u02fa\u02fb")
        buf.write("\7j\2\2\u02fb\u02fc\7{\2\2\u02fc\u02fd\7r\2\2\u02fd\u02fe")
        buf.write("\7g\2\2\u02fe\u02ff\7t\2\2\u02ff\u0300\7a\2\2\u0300\u0301")
        buf.write("\7c\2\2\u0301\u0302\7u\2\2\u0302\u0303\7u\2\2\u0303\u0304")
        buf.write("\7g\2\2\u0304\u0305\7t\2\2\u0305\u0306\7v\2\2\u0306\u00d6")
        buf.write("\3\2\2\2\u0307\u0309\t\3\2\2\u0308\u0307\3\2\2\2\u0309")
        buf.write("\u030a\3\2\2\2\u030a\u0308\3\2\2\2\u030a\u030b\3\2\2\2")
        buf.write("\u030b\u0310\3\2\2\2\u030c\u030d\7k\2\2\u030d\u030e\7")
        buf.write("p\2\2\u030e\u0310\7h\2\2\u030f\u0308\3\2\2\2\u030f\u030c")
        buf.write("\3\2\2\2\u0310\u00d8\3\2\2\2\u0311\u0315\t\4\2\2\u0312")
        buf.write("\u0314\t\5\2\2\u0313\u0312\3\2\2\2\u0314\u0317\3\2\2\2")
        buf.write("\u0315\u0313\3\2\2\2\u0315\u0316\3\2\2\2\u0316\u00da\3")
        buf.write("\2\2\2\u0317\u0315\3\2\2\2\u0318\u031b\t\6\2\2\u0319\u031c")
        buf.write("\5\u00ddo\2\u031a\u031c\5\u00d9m\2\u031b\u0319\3\2\2\2")
        buf.write("\u031b\u031a\3\2\2\2\u031c\u00dc\3\2\2\2\u031d\u031e\7")
        buf.write("\62\2\2\u031e\u031f\7Z\2\2\u031f\u0321\3\2\2\2\u0320\u0322")
        buf.write("\5\u00dfp\2\u0321\u0320\3\2\2\2\u0322\u0323\3\2\2\2\u0323")
        buf.write("\u0321\3\2\2\2\u0323\u0324\3\2\2\2\u0324\u00de\3\2\2\2")
        buf.write("\u0325\u0326\t\7\2\2\u0326\u00e0\3\2\2\2\u0327\u0328\7")
        buf.write("]\2\2\u0328\u0329\bq\6\2\u0329\u00e2\3\2\2\2\u032a\u032b")
        buf.write("\7_\2\2\u032b\u032c\br\7\2\u032c\u00e4\3\2\2\2\u032d\u032e")
        buf.write("\7}\2\2\u032e\u032f\bs\b\2\u032f\u00e6\3\2\2\2\u0330\u0331")
        buf.write("\7\177\2\2\u0331\u0332\bt\t\2\u0332\u00e8\3\2\2\2\u0333")
        buf.write("\u0334\7*\2\2\u0334\u0335\bu\n\2\u0335\u00ea\3\2\2\2\u0336")
        buf.write("\u0337\7+\2\2\u0337\u0338\bv\13\2\u0338\u00ec\3\2\2\2")
        buf.write("\u0339\u033a\7=\2\2\u033a\u00ee\3\2\2\2\u033b\u033e\5")
        buf.write("\u00f1y\2\u033c\u033e\5\u00f3z\2\u033d\u033b\3\2\2\2\u033d")
        buf.write("\u033c\3\2\2\2\u033e\u00f0\3\2\2\2\u033f\u0344\7)\2\2")
        buf.write("\u0340\u0343\5\u00f9}\2\u0341\u0343\n\b\2\2\u0342\u0340")
        buf.write("\3\2\2\2\u0342\u0341\3\2\2\2\u0343\u0346\3\2\2\2\u0344")
        buf.write("\u0342\3\2\2\2\u0344\u0345\3\2\2\2\u0345\u0347\3\2\2\2")
        buf.write("\u0346\u0344\3\2\2\2\u0347\u0352\7)\2\2\u0348\u034d\7")
        buf.write("$\2\2\u0349\u034c\5\u00f9}\2\u034a\u034c\n\t\2\2\u034b")
        buf.write("\u0349\3\2\2\2\u034b\u034a\3\2\2\2\u034c\u034f\3\2\2\2")
        buf.write("\u034d\u034b\3\2\2\2\u034d\u034e\3\2\2\2\u034e\u0350\3")
        buf.write("\2\2\2\u034f\u034d\3\2\2\2\u0350\u0352\7$\2\2\u0351\u033f")
        buf.write("\3\2\2\2\u0351\u0348\3\2\2\2\u0352\u00f2\3\2\2\2\u0353")
        buf.write("\u0354\7)\2\2\u0354\u0355\7)\2\2\u0355\u0356\7)\2\2\u0356")
        buf.write("\u035a\3\2\2\2\u0357\u0359\5\u00f5{\2\u0358\u0357\3\2")
        buf.write("\2\2\u0359\u035c\3\2\2\2\u035a\u035b\3\2\2\2\u035a\u0358")
        buf.write("\3\2\2\2\u035b\u035d\3\2\2\2\u035c\u035a\3\2\2\2\u035d")
        buf.write("\u035e\7)\2\2\u035e\u035f\7)\2\2\u035f\u036e\7)\2\2\u0360")
        buf.write("\u0361\7$\2\2\u0361\u0362\7$\2\2\u0362\u0363\7$\2\2\u0363")
        buf.write("\u0367\3\2\2\2\u0364\u0366\5\u00f5{\2\u0365\u0364\3\2")
        buf.write("\2\2\u0366\u0369\3\2\2\2\u0367\u0368\3\2\2\2\u0367\u0365")
        buf.write("\3\2\2\2\u0368\u036a\3\2\2\2\u0369\u0367\3\2\2\2\u036a")
        buf.write("\u036b\7$\2\2\u036b\u036c\7$\2\2\u036c\u036e\7$\2\2\u036d")
        buf.write("\u0353\3\2\2\2\u036d\u0360\3\2\2\2\u036e\u00f4\3\2\2\2")
        buf.write("\u036f\u0372\5\u00f7|\2\u0370\u0372\5\u00f9}\2\u0371\u036f")
        buf.write("\3\2\2\2\u0371\u0370\3\2\2\2\u0372\u00f6\3\2\2\2\u0373")
        buf.write("\u0374\n\n\2\2\u0374\u00f8\3\2\2\2\u0375\u0376\7^\2\2")
        buf.write("\u0376\u037a\13\2\2\2\u0377\u0378\7^\2\2\u0378\u037a\5")
        buf.write("o8\2\u0379\u0375\3\2\2\2\u0379\u0377\3\2\2\2\u037a\u00fa")
        buf.write("\3\2\2\2\36\2\u01d2\u01d8\u01de\u01e1\u01e8\u01ed\u01f2")
        buf.write("\u01fa\u0203\u0206\u02f0\u030a\u030f\u0315\u031b\u0323")
        buf.write("\u033d\u0342\u0344\u034b\u034d\u0351\u035a\u0367\u036d")
        buf.write("\u0371\u0379\f\38\2\b\2\2\3d\3\3e\4\3q\5\3r\6\3s\7\3t")
        buf.write("\b\3u\t\3v\n")
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
    SAVE = 70
    STOP = 71
    LAMBDA = 72
    ADDRESS_OF = 73
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
    HYPER = 105
    INT = 106
    NAME = 107
    ATOM = 108
    HEX_INTEGER = 109
    OPEN_BRACK = 110
    CLOSE_BRACK = 111
    OPEN_BRACES = 112
    CLOSE_BRACES = 113
    OPEN_PAREN = 114
    CLOSE_PAREN = 115
    SEMI_COLON = 116
    STRING = 117

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'or'", "'=>'", "'&'", "'|'", "'^'", "'-'", "'+'", 
            "'//'", "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", 
            "'!='", "'<'", "'<='", "'>'", "'>='", "'~'", "'abs'", "'atLabel'", 
            "'countLabel'", "'get_context'", "'contexts'", "'isEmpty'", 
            "'min'", "'max'", "'len'", "'type'", "'str'", "'any'", "'all'", 
            "'keys'", "'hash'", "'choose'", "'end'", "'and='", "'or='", 
            "'=>='", "'&='", "'|='", "'^='", "'-='", "'+='", "'*='", "'/='", 
            "'//='", "'%='", "'mod='", "'**='", "'>>='", "'#'", "'(*'", 
            "'*)'", "'!'", "'*'", "'as'", "'.'", "'import'", "'print'", 
            "'from'", "'..'", "'setintlevel'", "'->'", "'save'", "'stop'", 
            "'lambda'", "'?'", "'not'", "','", "'const'", "'await'", "'assert'", 
            "'var'", "'trap'", "'pass'", "'del'", "'spawn'", "'invariant'", 
            "'go'", "'sequential'", "'when'", "'let'", "'if'", "'elif'", 
            "'else'", "'@'", "'while'", "'def'", "'exists'", "'where'", 
            "'='", "'for'", "'in'", "':'", "'None'", "'atomically'", "'eternal'", 
            "'hyper_assert'", "'['", "']'", "'{'", "'}'", "'('", "')'", 
            "';'" ]

    symbolicNames = [ "<INVALID>",
            "NL", "WS", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
            "POINTER_OF", "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", 
            "RANGE", "SETINTLEVEL", "ARROW", "SAVE", "STOP", "LAMBDA", "ADDRESS_OF", 
            "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", "VAR", "TRAP", "PASS", 
            "DEL", "SPAWN", "INVARIANT", "GO", "SEQUENTIAL", "WHEN", "LET", 
            "IF", "ELIF", "ELSE", "AT", "WHILE", "DEF", "EXISTS", "WHERE", 
            "EQ", "FOR", "IN", "COLON", "NONE", "ATOMICALLY", "BOOL", "ETERNAL", 
            "HYPER", "INT", "NAME", "ATOM", "HEX_INTEGER", "OPEN_BRACK", 
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
                  "FROM", "RANGE", "SETINTLEVEL", "ARROW", "SAVE", "STOP", 
                  "LAMBDA", "ADDRESS_OF", "NOT", "COMMA", "CONST", "AWAIT", 
                  "ASSERT", "VAR", "TRAP", "PASS", "DEL", "SPAWN", "INVARIANT", 
                  "GO", "SEQUENTIAL", "WHEN", "LET", "IF", "ELIF", "ELSE", 
                  "AT", "WHILE", "DEF", "EXISTS", "WHERE", "EQ", "FOR", 
                  "IN", "COLON", "NONE", "ATOMICALLY", "BOOL", "ETERNAL", 
                  "HYPER", "INT", "NAME", "ATOM", "HEX_INTEGER", "HEX_DIGIT", 
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
            actions[54] = self.NL_action 
            actions[98] = self.FOR_action 
            actions[99] = self.IN_action 
            actions[111] = self.OPEN_BRACK_action 
            actions[112] = self.CLOSE_BRACK_action 
            actions[113] = self.OPEN_BRACES_action 
            actions[114] = self.CLOSE_BRACES_action 
            actions[115] = self.OPEN_PAREN_action 
            actions[116] = self.CLOSE_PAREN_action 
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
     


