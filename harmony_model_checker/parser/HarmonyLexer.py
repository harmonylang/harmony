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
        buf.write("\u0376\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("\3\34\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\36\3\36\3\36")
        buf.write("\3\36\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3 \3!\3!\3!\3!\3")
        buf.write("\"\3\"\3\"\3\"\3#\3#\3#\3#\3$\3$\3$\3$\3$\3%\3%\3%\3%")
        buf.write("\3%\3&\3&\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3")
        buf.write("(\3)\3)\3)\3)\3*\3*\3*\3*\3+\3+\3+\3,\3,\3,\3-\3-\3-\3")
        buf.write(".\3.\3.\3/\3/\3/\3\60\3\60\3\60\3\61\3\61\3\61\3\62\3")
        buf.write("\62\3\62\3\62\3\63\3\63\3\63\3\64\3\64\3\64\3\64\3\64")
        buf.write("\3\65\3\65\3\65\3\65\3\66\3\66\3\66\3\66\3\67\5\67\u01cb")
        buf.write("\n\67\3\67\3\67\7\67\u01cf\n\67\f\67\16\67\u01d2\13\67")
        buf.write("\3\67\7\67\u01d5\n\67\f\67\16\67\u01d8\13\67\5\67\u01da")
        buf.write("\n\67\3\67\3\67\38\68\u01df\n8\r8\168\u01e0\38\68\u01e4")
        buf.write("\n8\r8\168\u01e5\38\38\38\58\u01eb\n8\38\38\39\39\79\u01f1")
        buf.write("\n9\f9\169\u01f4\139\39\39\39\39\79\u01fa\n9\f9\169\u01fd")
        buf.write("\139\59\u01ff\n9\3:\3:\3;\3;\3;\3<\3<\3<\3=\3=\3>\3>\3")
        buf.write("?\3?\3?\3@\3@\3A\3A\3A\3A\3A\3A\3A\3B\3B\3B\3B\3B\3B\3")
        buf.write("C\3C\3C\3C\3C\3D\3D\3D\3E\3E\3E\3E\3E\3E\3E\3E\3E\3E\3")
        buf.write("E\3E\3F\3F\3F\3G\3G\3G\3G\3G\3H\3H\3H\3H\3H\3I\3I\3I\3")
        buf.write("I\3I\3I\3I\3J\3J\3K\3K\3K\3K\3L\3L\3M\3M\3M\3M\3M\3M\3")
        buf.write("N\3N\3N\3N\3N\3N\3O\3O\3O\3O\3O\3O\3O\3P\3P\3P\3P\3Q\3")
        buf.write("Q\3Q\3Q\3Q\3R\3R\3R\3R\3R\3S\3S\3S\3S\3T\3T\3T\3T\3T\3")
        buf.write("T\3U\3U\3U\3U\3U\3U\3U\3U\3U\3U\3V\3V\3V\3W\3W\3W\3W\3")
        buf.write("W\3W\3W\3W\3X\3X\3X\3X\3X\3X\3X\3X\3X\3X\3X\3Y\3Y\3Y\3")
        buf.write("Y\3Y\3Z\3Z\3Z\3Z\3[\3[\3[\3\\\3\\\3\\\3\\\3\\\3]\3]\3")
        buf.write("]\3]\3]\3^\3^\3_\3_\3_\3_\3_\3_\3`\3`\3`\3`\3a\3a\3a\3")
        buf.write("a\3a\3a\3a\3a\3b\3b\3b\3b\3b\3b\3b\3c\3c\3c\3c\3c\3c\3")
        buf.write("d\3d\3e\3e\3e\3e\3e\3e\3f\3f\3f\3f\3f\3g\3g\3h\3h\3h\3")
        buf.write("h\3h\3i\3i\3i\3i\3i\3i\3i\3i\3i\3i\3i\3j\3j\3j\3j\3j\3")
        buf.write("j\3j\3j\3j\5j\u02f9\nj\3k\3k\3k\3k\3k\3k\3k\3k\3l\6l\u0304")
        buf.write("\nl\rl\16l\u0305\3l\3l\3l\5l\u030b\nl\3m\3m\7m\u030f\n")
        buf.write("m\fm\16m\u0312\13m\3n\3n\3n\5n\u0317\nn\3o\3o\3o\3o\6")
        buf.write("o\u031d\no\ro\16o\u031e\3p\3p\3q\3q\3q\3r\3r\3r\3s\3s")
        buf.write("\3s\3t\3t\3t\3u\3u\3u\3v\3v\3v\3w\3w\3x\3x\5x\u0339\n")
        buf.write("x\3y\3y\3y\7y\u033e\ny\fy\16y\u0341\13y\3y\3y\3y\3y\7")
        buf.write("y\u0347\ny\fy\16y\u034a\13y\3y\5y\u034d\ny\3z\3z\3z\3")
        buf.write("z\3z\7z\u0354\nz\fz\16z\u0357\13z\3z\3z\3z\3z\3z\3z\3")
        buf.write("z\3z\7z\u0361\nz\fz\16z\u0364\13z\3z\3z\3z\5z\u0369\n")
        buf.write("z\3{\3{\5{\u036d\n{\3|\3|\3}\3}\3}\3}\5}\u0375\n}\5\u01f2")
        buf.write("\u0355\u0362\2~\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23")
        buf.write("\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25")
        buf.write(")\26+\27-\30/\31\61\32\63\33\65\34\67\359\36;\37= ?!A")
        buf.write("\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63e\64g\65")
        buf.write("i\66k\67m8o9q\2s:u;w<y={>}?\177@\u0081A\u0083B\u0085C")
        buf.write("\u0087D\u0089E\u008bF\u008dG\u008fH\u0091I\u0093J\u0095")
        buf.write("K\u0097L\u0099M\u009bN\u009dO\u009fP\u00a1Q\u00a3R\u00a5")
        buf.write("S\u00a7T\u00a9U\u00abV\u00adW\u00afX\u00b1Y\u00b3Z\u00b5")
        buf.write("[\u00b7\\\u00b9]\u00bb^\u00bd_\u00bf`\u00c1a\u00c3b\u00c5")
        buf.write("c\u00c7d\u00c9e\u00cbf\u00cdg\u00cfh\u00d1i\u00d3j\u00d5")
        buf.write("k\u00d7l\u00d9m\u00dbn\u00ddo\u00df\2\u00e1p\u00e3q\u00e5")
        buf.write("r\u00e7s\u00e9t\u00ebu\u00edv\u00efw\u00f1\2\u00f3\2\u00f5")
        buf.write("\2\u00f7\2\u00f9\2\3\2\13\4\2\f\f\16\17\3\2\62;\5\2C\\")
        buf.write("aac|\6\2\62;C\\aac|\3\2\60\60\5\2\62;CHch\6\2\f\f\16\17")
        buf.write("))^^\6\2\f\f\16\17$$^^\3\2^^\2\u038b\2\3\3\2\2\2\2\5\3")
        buf.write("\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2")
        buf.write("\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2")
        buf.write("\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2")
        buf.write("\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2")
        buf.write("\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3")
        buf.write("\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2")
        buf.write("\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2")
        buf.write("\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3")
        buf.write("\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W")
        buf.write("\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2")
        buf.write("a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2")
        buf.write("\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2s\3\2\2\2\2u\3\2\2")
        buf.write("\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3")
        buf.write("\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085\3\2\2\2")
        buf.write("\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2\u008b\3\2\2\2\2\u008d")
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
        buf.write("\2\2\u00db\3\2\2\2\2\u00dd\3\2\2\2\2\u00e1\3\2\2\2\2\u00e3")
        buf.write("\3\2\2\2\2\u00e5\3\2\2\2\2\u00e7\3\2\2\2\2\u00e9\3\2\2")
        buf.write("\2\2\u00eb\3\2\2\2\2\u00ed\3\2\2\2\2\u00ef\3\2\2\2\3\u00fb")
        buf.write("\3\2\2\2\5\u00ff\3\2\2\2\7\u0102\3\2\2\2\t\u0105\3\2\2")
        buf.write("\2\13\u0107\3\2\2\2\r\u0109\3\2\2\2\17\u010b\3\2\2\2\21")
        buf.write("\u010d\3\2\2\2\23\u010f\3\2\2\2\25\u0112\3\2\2\2\27\u0114")
        buf.write("\3\2\2\2\31\u0116\3\2\2\2\33\u011a\3\2\2\2\35\u011d\3")
        buf.write("\2\2\2\37\u0120\3\2\2\2!\u0123\3\2\2\2#\u0126\3\2\2\2")
        buf.write("%\u0129\3\2\2\2\'\u012b\3\2\2\2)\u012e\3\2\2\2+\u0130")
        buf.write("\3\2\2\2-\u0133\3\2\2\2/\u0135\3\2\2\2\61\u0139\3\2\2")
        buf.write("\2\63\u0141\3\2\2\2\65\u014c\3\2\2\2\67\u0158\3\2\2\2")
        buf.write("9\u0161\3\2\2\2;\u0165\3\2\2\2=\u0169\3\2\2\2?\u016d\3")
        buf.write("\2\2\2A\u0172\3\2\2\2C\u0176\3\2\2\2E\u017a\3\2\2\2G\u017e")
        buf.write("\3\2\2\2I\u0183\3\2\2\2K\u0188\3\2\2\2M\u018f\3\2\2\2")
        buf.write("O\u0193\3\2\2\2Q\u0198\3\2\2\2S\u019c\3\2\2\2U\u01a0\3")
        buf.write("\2\2\2W\u01a3\3\2\2\2Y\u01a6\3\2\2\2[\u01a9\3\2\2\2]\u01ac")
        buf.write("\3\2\2\2_\u01af\3\2\2\2a\u01b2\3\2\2\2c\u01b5\3\2\2\2")
        buf.write("e\u01b9\3\2\2\2g\u01bc\3\2\2\2i\u01c1\3\2\2\2k\u01c5\3")
        buf.write("\2\2\2m\u01ca\3\2\2\2o\u01ea\3\2\2\2q\u01fe\3\2\2\2s\u0200")
        buf.write("\3\2\2\2u\u0202\3\2\2\2w\u0205\3\2\2\2y\u0208\3\2\2\2")
        buf.write("{\u020a\3\2\2\2}\u020c\3\2\2\2\177\u020f\3\2\2\2\u0081")
        buf.write("\u0211\3\2\2\2\u0083\u0218\3\2\2\2\u0085\u021e\3\2\2\2")
        buf.write("\u0087\u0223\3\2\2\2\u0089\u0226\3\2\2\2\u008b\u0232\3")
        buf.write("\2\2\2\u008d\u0235\3\2\2\2\u008f\u023a\3\2\2\2\u0091\u023f")
        buf.write("\3\2\2\2\u0093\u0246\3\2\2\2\u0095\u0248\3\2\2\2\u0097")
        buf.write("\u024c\3\2\2\2\u0099\u024e\3\2\2\2\u009b\u0254\3\2\2\2")
        buf.write("\u009d\u025a\3\2\2\2\u009f\u0261\3\2\2\2\u00a1\u0265\3")
        buf.write("\2\2\2\u00a3\u026a\3\2\2\2\u00a5\u026f\3\2\2\2\u00a7\u0273")
        buf.write("\3\2\2\2\u00a9\u0279\3\2\2\2\u00ab\u0283\3\2\2\2\u00ad")
        buf.write("\u0286\3\2\2\2\u00af\u028e\3\2\2\2\u00b1\u0299\3\2\2\2")
        buf.write("\u00b3\u029e\3\2\2\2\u00b5\u02a2\3\2\2\2\u00b7\u02a5\3")
        buf.write("\2\2\2\u00b9\u02aa\3\2\2\2\u00bb\u02af\3\2\2\2\u00bd\u02b1")
        buf.write("\3\2\2\2\u00bf\u02b7\3\2\2\2\u00c1\u02bb\3\2\2\2\u00c3")
        buf.write("\u02c3\3\2\2\2\u00c5\u02ca\3\2\2\2\u00c7\u02d0\3\2\2\2")
        buf.write("\u00c9\u02d2\3\2\2\2\u00cb\u02d8\3\2\2\2\u00cd\u02dd\3")
        buf.write("\2\2\2\u00cf\u02df\3\2\2\2\u00d1\u02e4\3\2\2\2\u00d3\u02f8")
        buf.write("\3\2\2\2\u00d5\u02fa\3\2\2\2\u00d7\u030a\3\2\2\2\u00d9")
        buf.write("\u030c\3\2\2\2\u00db\u0313\3\2\2\2\u00dd\u0318\3\2\2\2")
        buf.write("\u00df\u0320\3\2\2\2\u00e1\u0322\3\2\2\2\u00e3\u0325\3")
        buf.write("\2\2\2\u00e5\u0328\3\2\2\2\u00e7\u032b\3\2\2\2\u00e9\u032e")
        buf.write("\3\2\2\2\u00eb\u0331\3\2\2\2\u00ed\u0334\3\2\2\2\u00ef")
        buf.write("\u0338\3\2\2\2\u00f1\u034c\3\2\2\2\u00f3\u0368\3\2\2\2")
        buf.write("\u00f5\u036c\3\2\2\2\u00f7\u036e\3\2\2\2\u00f9\u0374\3")
        buf.write("\2\2\2\u00fb\u00fc\7c\2\2\u00fc\u00fd\7p\2\2\u00fd\u00fe")
        buf.write("\7f\2\2\u00fe\4\3\2\2\2\u00ff\u0100\7q\2\2\u0100\u0101")
        buf.write("\7t\2\2\u0101\6\3\2\2\2\u0102\u0103\7?\2\2\u0103\u0104")
        buf.write("\7@\2\2\u0104\b\3\2\2\2\u0105\u0106\7(\2\2\u0106\n\3\2")
        buf.write("\2\2\u0107\u0108\7~\2\2\u0108\f\3\2\2\2\u0109\u010a\7")
        buf.write("`\2\2\u010a\16\3\2\2\2\u010b\u010c\7/\2\2\u010c\20\3\2")
        buf.write("\2\2\u010d\u010e\7-\2\2\u010e\22\3\2\2\2\u010f\u0110\7")
        buf.write("\61\2\2\u0110\u0111\7\61\2\2\u0111\24\3\2\2\2\u0112\u0113")
        buf.write("\7\61\2\2\u0113\26\3\2\2\2\u0114\u0115\7\'\2\2\u0115\30")
        buf.write("\3\2\2\2\u0116\u0117\7o\2\2\u0117\u0118\7q\2\2\u0118\u0119")
        buf.write("\7f\2\2\u0119\32\3\2\2\2\u011a\u011b\7,\2\2\u011b\u011c")
        buf.write("\7,\2\2\u011c\34\3\2\2\2\u011d\u011e\7>\2\2\u011e\u011f")
        buf.write("\7>\2\2\u011f\36\3\2\2\2\u0120\u0121\7@\2\2\u0121\u0122")
        buf.write("\7@\2\2\u0122 \3\2\2\2\u0123\u0124\7?\2\2\u0124\u0125")
        buf.write("\7?\2\2\u0125\"\3\2\2\2\u0126\u0127\7#\2\2\u0127\u0128")
        buf.write("\7?\2\2\u0128$\3\2\2\2\u0129\u012a\7>\2\2\u012a&\3\2\2")
        buf.write("\2\u012b\u012c\7>\2\2\u012c\u012d\7?\2\2\u012d(\3\2\2")
        buf.write("\2\u012e\u012f\7@\2\2\u012f*\3\2\2\2\u0130\u0131\7@\2")
        buf.write("\2\u0131\u0132\7?\2\2\u0132,\3\2\2\2\u0133\u0134\7\u0080")
        buf.write("\2\2\u0134.\3\2\2\2\u0135\u0136\7c\2\2\u0136\u0137\7d")
        buf.write("\2\2\u0137\u0138\7u\2\2\u0138\60\3\2\2\2\u0139\u013a\7")
        buf.write("c\2\2\u013a\u013b\7v\2\2\u013b\u013c\7N\2\2\u013c\u013d")
        buf.write("\7c\2\2\u013d\u013e\7d\2\2\u013e\u013f\7g\2\2\u013f\u0140")
        buf.write("\7n\2\2\u0140\62\3\2\2\2\u0141\u0142\7e\2\2\u0142\u0143")
        buf.write("\7q\2\2\u0143\u0144\7w\2\2\u0144\u0145\7p\2\2\u0145\u0146")
        buf.write("\7v\2\2\u0146\u0147\7N\2\2\u0147\u0148\7c\2\2\u0148\u0149")
        buf.write("\7d\2\2\u0149\u014a\7g\2\2\u014a\u014b\7n\2\2\u014b\64")
        buf.write("\3\2\2\2\u014c\u014d\7i\2\2\u014d\u014e\7g\2\2\u014e\u014f")
        buf.write("\7v\2\2\u014f\u0150\7a\2\2\u0150\u0151\7e\2\2\u0151\u0152")
        buf.write("\7q\2\2\u0152\u0153\7p\2\2\u0153\u0154\7v\2\2\u0154\u0155")
        buf.write("\7g\2\2\u0155\u0156\7z\2\2\u0156\u0157\7v\2\2\u0157\66")
        buf.write("\3\2\2\2\u0158\u0159\7e\2\2\u0159\u015a\7q\2\2\u015a\u015b")
        buf.write("\7p\2\2\u015b\u015c\7v\2\2\u015c\u015d\7g\2\2\u015d\u015e")
        buf.write("\7z\2\2\u015e\u015f\7v\2\2\u015f\u0160\7u\2\2\u01608\3")
        buf.write("\2\2\2\u0161\u0162\7o\2\2\u0162\u0163\7k\2\2\u0163\u0164")
        buf.write("\7p\2\2\u0164:\3\2\2\2\u0165\u0166\7o\2\2\u0166\u0167")
        buf.write("\7c\2\2\u0167\u0168\7z\2\2\u0168<\3\2\2\2\u0169\u016a")
        buf.write("\7n\2\2\u016a\u016b\7g\2\2\u016b\u016c\7p\2\2\u016c>\3")
        buf.write("\2\2\2\u016d\u016e\7v\2\2\u016e\u016f\7{\2\2\u016f\u0170")
        buf.write("\7r\2\2\u0170\u0171\7g\2\2\u0171@\3\2\2\2\u0172\u0173")
        buf.write("\7u\2\2\u0173\u0174\7v\2\2\u0174\u0175\7t\2\2\u0175B\3")
        buf.write("\2\2\2\u0176\u0177\7c\2\2\u0177\u0178\7p\2\2\u0178\u0179")
        buf.write("\7{\2\2\u0179D\3\2\2\2\u017a\u017b\7c\2\2\u017b\u017c")
        buf.write("\7n\2\2\u017c\u017d\7n\2\2\u017dF\3\2\2\2\u017e\u017f")
        buf.write("\7m\2\2\u017f\u0180\7g\2\2\u0180\u0181\7{\2\2\u0181\u0182")
        buf.write("\7u\2\2\u0182H\3\2\2\2\u0183\u0184\7j\2\2\u0184\u0185")
        buf.write("\7c\2\2\u0185\u0186\7u\2\2\u0186\u0187\7j\2\2\u0187J\3")
        buf.write("\2\2\2\u0188\u0189\7e\2\2\u0189\u018a\7j\2\2\u018a\u018b")
        buf.write("\7q\2\2\u018b\u018c\7q\2\2\u018c\u018d\7u\2\2\u018d\u018e")
        buf.write("\7g\2\2\u018eL\3\2\2\2\u018f\u0190\7g\2\2\u0190\u0191")
        buf.write("\7p\2\2\u0191\u0192\7f\2\2\u0192N\3\2\2\2\u0193\u0194")
        buf.write("\7c\2\2\u0194\u0195\7p\2\2\u0195\u0196\7f\2\2\u0196\u0197")
        buf.write("\7?\2\2\u0197P\3\2\2\2\u0198\u0199\7q\2\2\u0199\u019a")
        buf.write("\7t\2\2\u019a\u019b\7?\2\2\u019bR\3\2\2\2\u019c\u019d")
        buf.write("\7?\2\2\u019d\u019e\7@\2\2\u019e\u019f\7?\2\2\u019fT\3")
        buf.write("\2\2\2\u01a0\u01a1\7(\2\2\u01a1\u01a2\7?\2\2\u01a2V\3")
        buf.write("\2\2\2\u01a3\u01a4\7~\2\2\u01a4\u01a5\7?\2\2\u01a5X\3")
        buf.write("\2\2\2\u01a6\u01a7\7`\2\2\u01a7\u01a8\7?\2\2\u01a8Z\3")
        buf.write("\2\2\2\u01a9\u01aa\7/\2\2\u01aa\u01ab\7?\2\2\u01ab\\\3")
        buf.write("\2\2\2\u01ac\u01ad\7-\2\2\u01ad\u01ae\7?\2\2\u01ae^\3")
        buf.write("\2\2\2\u01af\u01b0\7,\2\2\u01b0\u01b1\7?\2\2\u01b1`\3")
        buf.write("\2\2\2\u01b2\u01b3\7\61\2\2\u01b3\u01b4\7?\2\2\u01b4b")
        buf.write("\3\2\2\2\u01b5\u01b6\7\61\2\2\u01b6\u01b7\7\61\2\2\u01b7")
        buf.write("\u01b8\7?\2\2\u01b8d\3\2\2\2\u01b9\u01ba\7\'\2\2\u01ba")
        buf.write("\u01bb\7?\2\2\u01bbf\3\2\2\2\u01bc\u01bd\7o\2\2\u01bd")
        buf.write("\u01be\7q\2\2\u01be\u01bf\7f\2\2\u01bf\u01c0\7?\2\2\u01c0")
        buf.write("h\3\2\2\2\u01c1\u01c2\7,\2\2\u01c2\u01c3\7,\2\2\u01c3")
        buf.write("\u01c4\7?\2\2\u01c4j\3\2\2\2\u01c5\u01c6\7@\2\2\u01c6")
        buf.write("\u01c7\7@\2\2\u01c7\u01c8\7?\2\2\u01c8l\3\2\2\2\u01c9")
        buf.write("\u01cb\7\17\2\2\u01ca\u01c9\3\2\2\2\u01ca\u01cb\3\2\2")
        buf.write("\2\u01cb\u01cc\3\2\2\2\u01cc\u01d9\7\f\2\2\u01cd\u01cf")
        buf.write("\7\"\2\2\u01ce\u01cd\3\2\2\2\u01cf\u01d2\3\2\2\2\u01d0")
        buf.write("\u01ce\3\2\2\2\u01d0\u01d1\3\2\2\2\u01d1\u01da\3\2\2\2")
        buf.write("\u01d2\u01d0\3\2\2\2\u01d3\u01d5\7\13\2\2\u01d4\u01d3")
        buf.write("\3\2\2\2\u01d5\u01d8\3\2\2\2\u01d6\u01d4\3\2\2\2\u01d6")
        buf.write("\u01d7\3\2\2\2\u01d7\u01da\3\2\2\2\u01d8\u01d6\3\2\2\2")
        buf.write("\u01d9\u01d0\3\2\2\2\u01d9\u01d6\3\2\2\2\u01da\u01db\3")
        buf.write("\2\2\2\u01db\u01dc\b\67\2\2\u01dcn\3\2\2\2\u01dd\u01df")
        buf.write("\7\"\2\2\u01de\u01dd\3\2\2\2\u01df\u01e0\3\2\2\2\u01e0")
        buf.write("\u01de\3\2\2\2\u01e0\u01e1\3\2\2\2\u01e1\u01eb\3\2\2\2")
        buf.write("\u01e2\u01e4\7\13\2\2\u01e3\u01e2\3\2\2\2\u01e4\u01e5")
        buf.write("\3\2\2\2\u01e5\u01e3\3\2\2\2\u01e5\u01e6\3\2\2\2\u01e6")
        buf.write("\u01eb\3\2\2\2\u01e7\u01e8\7^\2\2\u01e8\u01eb\5m\67\2")
        buf.write("\u01e9\u01eb\5q9\2\u01ea\u01de\3\2\2\2\u01ea\u01e3\3\2")
        buf.write("\2\2\u01ea\u01e7\3\2\2\2\u01ea\u01e9\3\2\2\2\u01eb\u01ec")
        buf.write("\3\2\2\2\u01ec\u01ed\b8\3\2\u01edp\3\2\2\2\u01ee\u01f2")
        buf.write("\5u;\2\u01ef\u01f1\13\2\2\2\u01f0\u01ef\3\2\2\2\u01f1")
        buf.write("\u01f4\3\2\2\2\u01f2\u01f3\3\2\2\2\u01f2\u01f0\3\2\2\2")
        buf.write("\u01f3\u01f5\3\2\2\2\u01f4\u01f2\3\2\2\2\u01f5\u01f6\5")
        buf.write("w<\2\u01f6\u01ff\3\2\2\2\u01f7\u01fb\5s:\2\u01f8\u01fa")
        buf.write("\n\2\2\2\u01f9\u01f8\3\2\2\2\u01fa\u01fd\3\2\2\2\u01fb")
        buf.write("\u01f9\3\2\2\2\u01fb\u01fc\3\2\2\2\u01fc\u01ff\3\2\2\2")
        buf.write("\u01fd\u01fb\3\2\2\2\u01fe\u01ee\3\2\2\2\u01fe\u01f7\3")
        buf.write("\2\2\2\u01ffr\3\2\2\2\u0200\u0201\7%\2\2\u0201t\3\2\2")
        buf.write("\2\u0202\u0203\7*\2\2\u0203\u0204\7,\2\2\u0204v\3\2\2")
        buf.write("\2\u0205\u0206\7,\2\2\u0206\u0207\7+\2\2\u0207x\3\2\2")
        buf.write("\2\u0208\u0209\7#\2\2\u0209z\3\2\2\2\u020a\u020b\7,\2")
        buf.write("\2\u020b|\3\2\2\2\u020c\u020d\7c\2\2\u020d\u020e\7u\2")
        buf.write("\2\u020e~\3\2\2\2\u020f\u0210\7\60\2\2\u0210\u0080\3\2")
        buf.write("\2\2\u0211\u0212\7k\2\2\u0212\u0213\7o\2\2\u0213\u0214")
        buf.write("\7r\2\2\u0214\u0215\7q\2\2\u0215\u0216\7t\2\2\u0216\u0217")
        buf.write("\7v\2\2\u0217\u0082\3\2\2\2\u0218\u0219\7r\2\2\u0219\u021a")
        buf.write("\7t\2\2\u021a\u021b\7k\2\2\u021b\u021c\7p\2\2\u021c\u021d")
        buf.write("\7v\2\2\u021d\u0084\3\2\2\2\u021e\u021f\7h\2\2\u021f\u0220")
        buf.write("\7t\2\2\u0220\u0221\7q\2\2\u0221\u0222\7o\2\2\u0222\u0086")
        buf.write("\3\2\2\2\u0223\u0224\7\60\2\2\u0224\u0225\7\60\2\2\u0225")
        buf.write("\u0088\3\2\2\2\u0226\u0227\7u\2\2\u0227\u0228\7g\2\2\u0228")
        buf.write("\u0229\7v\2\2\u0229\u022a\7k\2\2\u022a\u022b\7p\2\2\u022b")
        buf.write("\u022c\7v\2\2\u022c\u022d\7n\2\2\u022d\u022e\7g\2\2\u022e")
        buf.write("\u022f\7x\2\2\u022f\u0230\7g\2\2\u0230\u0231\7n\2\2\u0231")
        buf.write("\u008a\3\2\2\2\u0232\u0233\7/\2\2\u0233\u0234\7@\2\2\u0234")
        buf.write("\u008c\3\2\2\2\u0235\u0236\7u\2\2\u0236\u0237\7c\2\2\u0237")
        buf.write("\u0238\7x\2\2\u0238\u0239\7g\2\2\u0239\u008e\3\2\2\2\u023a")
        buf.write("\u023b\7u\2\2\u023b\u023c\7v\2\2\u023c\u023d\7q\2\2\u023d")
        buf.write("\u023e\7r\2\2\u023e\u0090\3\2\2\2\u023f\u0240\7n\2\2\u0240")
        buf.write("\u0241\7c\2\2\u0241\u0242\7o\2\2\u0242\u0243\7d\2\2\u0243")
        buf.write("\u0244\7f\2\2\u0244\u0245\7c\2\2\u0245\u0092\3\2\2\2\u0246")
        buf.write("\u0247\7A\2\2\u0247\u0094\3\2\2\2\u0248\u0249\7p\2\2\u0249")
        buf.write("\u024a\7q\2\2\u024a\u024b\7v\2\2\u024b\u0096\3\2\2\2\u024c")
        buf.write("\u024d\7.\2\2\u024d\u0098\3\2\2\2\u024e\u024f\7e\2\2\u024f")
        buf.write("\u0250\7q\2\2\u0250\u0251\7p\2\2\u0251\u0252\7u\2\2\u0252")
        buf.write("\u0253\7v\2\2\u0253\u009a\3\2\2\2\u0254\u0255\7c\2\2\u0255")
        buf.write("\u0256\7y\2\2\u0256\u0257\7c\2\2\u0257\u0258\7k\2\2\u0258")
        buf.write("\u0259\7v\2\2\u0259\u009c\3\2\2\2\u025a\u025b\7c\2\2\u025b")
        buf.write("\u025c\7u\2\2\u025c\u025d\7u\2\2\u025d\u025e\7g\2\2\u025e")
        buf.write("\u025f\7t\2\2\u025f\u0260\7v\2\2\u0260\u009e\3\2\2\2\u0261")
        buf.write("\u0262\7x\2\2\u0262\u0263\7c\2\2\u0263\u0264\7t\2\2\u0264")
        buf.write("\u00a0\3\2\2\2\u0265\u0266\7v\2\2\u0266\u0267\7t\2\2\u0267")
        buf.write("\u0268\7c\2\2\u0268\u0269\7r\2\2\u0269\u00a2\3\2\2\2\u026a")
        buf.write("\u026b\7r\2\2\u026b\u026c\7c\2\2\u026c\u026d\7u\2\2\u026d")
        buf.write("\u026e\7u\2\2\u026e\u00a4\3\2\2\2\u026f\u0270\7f\2\2\u0270")
        buf.write("\u0271\7g\2\2\u0271\u0272\7n\2\2\u0272\u00a6\3\2\2\2\u0273")
        buf.write("\u0274\7u\2\2\u0274\u0275\7r\2\2\u0275\u0276\7c\2\2\u0276")
        buf.write("\u0277\7y\2\2\u0277\u0278\7p\2\2\u0278\u00a8\3\2\2\2\u0279")
        buf.write("\u027a\7k\2\2\u027a\u027b\7p\2\2\u027b\u027c\7x\2\2\u027c")
        buf.write("\u027d\7c\2\2\u027d\u027e\7t\2\2\u027e\u027f\7k\2\2\u027f")
        buf.write("\u0280\7c\2\2\u0280\u0281\7p\2\2\u0281\u0282\7v\2\2\u0282")
        buf.write("\u00aa\3\2\2\2\u0283\u0284\7i\2\2\u0284\u0285\7q\2\2\u0285")
        buf.write("\u00ac\3\2\2\2\u0286\u0287\7d\2\2\u0287\u0288\7w\2\2\u0288")
        buf.write("\u0289\7k\2\2\u0289\u028a\7n\2\2\u028a\u028b\7v\2\2\u028b")
        buf.write("\u028c\7k\2\2\u028c\u028d\7p\2\2\u028d\u00ae\3\2\2\2\u028e")
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
        buf.write("\u02bc\7t\2\2\u02bc\u02bd\7g\2\2\u02bd\u02be\7v\2\2\u02be")
        buf.write("\u02bf\7w\2\2\u02bf\u02c0\7t\2\2\u02c0\u02c1\7p\2\2\u02c1")
        buf.write("\u02c2\7u\2\2\u02c2\u00c2\3\2\2\2\u02c3\u02c4\7g\2\2\u02c4")
        buf.write("\u02c5\7z\2\2\u02c5\u02c6\7k\2\2\u02c6\u02c7\7u\2\2\u02c7")
        buf.write("\u02c8\7v\2\2\u02c8\u02c9\7u\2\2\u02c9\u00c4\3\2\2\2\u02ca")
        buf.write("\u02cb\7y\2\2\u02cb\u02cc\7j\2\2\u02cc\u02cd\7g\2\2\u02cd")
        buf.write("\u02ce\7t\2\2\u02ce\u02cf\7g\2\2\u02cf\u00c6\3\2\2\2\u02d0")
        buf.write("\u02d1\7?\2\2\u02d1\u00c8\3\2\2\2\u02d2\u02d3\7h\2\2\u02d3")
        buf.write("\u02d4\7q\2\2\u02d4\u02d5\7t\2\2\u02d5\u02d6\3\2\2\2\u02d6")
        buf.write("\u02d7\be\4\2\u02d7\u00ca\3\2\2\2\u02d8\u02d9\7k\2\2\u02d9")
        buf.write("\u02da\7p\2\2\u02da\u02db\3\2\2\2\u02db\u02dc\bf\5\2\u02dc")
        buf.write("\u00cc\3\2\2\2\u02dd\u02de\7<\2\2\u02de\u00ce\3\2\2\2")
        buf.write("\u02df\u02e0\7P\2\2\u02e0\u02e1\7q\2\2\u02e1\u02e2\7p")
        buf.write("\2\2\u02e2\u02e3\7g\2\2\u02e3\u00d0\3\2\2\2\u02e4\u02e5")
        buf.write("\7c\2\2\u02e5\u02e6\7v\2\2\u02e6\u02e7\7q\2\2\u02e7\u02e8")
        buf.write("\7o\2\2\u02e8\u02e9\7k\2\2\u02e9\u02ea\7e\2\2\u02ea\u02eb")
        buf.write("\7c\2\2\u02eb\u02ec\7n\2\2\u02ec\u02ed\7n\2\2\u02ed\u02ee")
        buf.write("\7{\2\2\u02ee\u00d2\3\2\2\2\u02ef\u02f0\7H\2\2\u02f0\u02f1")
        buf.write("\7c\2\2\u02f1\u02f2\7n\2\2\u02f2\u02f3\7u\2\2\u02f3\u02f9")
        buf.write("\7g\2\2\u02f4\u02f5\7V\2\2\u02f5\u02f6\7t\2\2\u02f6\u02f7")
        buf.write("\7w\2\2\u02f7\u02f9\7g\2\2\u02f8\u02ef\3\2\2\2\u02f8\u02f4")
        buf.write("\3\2\2\2\u02f9\u00d4\3\2\2\2\u02fa\u02fb\7g\2\2\u02fb")
        buf.write("\u02fc\7v\2\2\u02fc\u02fd\7g\2\2\u02fd\u02fe\7t\2\2\u02fe")
        buf.write("\u02ff\7p\2\2\u02ff\u0300\7c\2\2\u0300\u0301\7n\2\2\u0301")
        buf.write("\u00d6\3\2\2\2\u0302\u0304\t\3\2\2\u0303\u0302\3\2\2\2")
        buf.write("\u0304\u0305\3\2\2\2\u0305\u0303\3\2\2\2\u0305\u0306\3")
        buf.write("\2\2\2\u0306\u030b\3\2\2\2\u0307\u0308\7k\2\2\u0308\u0309")
        buf.write("\7p\2\2\u0309\u030b\7h\2\2\u030a\u0303\3\2\2\2\u030a\u0307")
        buf.write("\3\2\2\2\u030b\u00d8\3\2\2\2\u030c\u0310\t\4\2\2\u030d")
        buf.write("\u030f\t\5\2\2\u030e\u030d\3\2\2\2\u030f\u0312\3\2\2\2")
        buf.write("\u0310\u030e\3\2\2\2\u0310\u0311\3\2\2\2\u0311\u00da\3")
        buf.write("\2\2\2\u0312\u0310\3\2\2\2\u0313\u0316\t\6\2\2\u0314\u0317")
        buf.write("\5\u00ddo\2\u0315\u0317\5\u00d9m\2\u0316\u0314\3\2\2\2")
        buf.write("\u0316\u0315\3\2\2\2\u0317\u00dc\3\2\2\2\u0318\u0319\7")
        buf.write("\62\2\2\u0319\u031a\7Z\2\2\u031a\u031c\3\2\2\2\u031b\u031d")
        buf.write("\5\u00dfp\2\u031c\u031b\3\2\2\2\u031d\u031e\3\2\2\2\u031e")
        buf.write("\u031c\3\2\2\2\u031e\u031f\3\2\2\2\u031f\u00de\3\2\2\2")
        buf.write("\u0320\u0321\t\7\2\2\u0321\u00e0\3\2\2\2\u0322\u0323\7")
        buf.write("]\2\2\u0323\u0324\bq\6\2\u0324\u00e2\3\2\2\2\u0325\u0326")
        buf.write("\7_\2\2\u0326\u0327\br\7\2\u0327\u00e4\3\2\2\2\u0328\u0329")
        buf.write("\7}\2\2\u0329\u032a\bs\b\2\u032a\u00e6\3\2\2\2\u032b\u032c")
        buf.write("\7\177\2\2\u032c\u032d\bt\t\2\u032d\u00e8\3\2\2\2\u032e")
        buf.write("\u032f\7*\2\2\u032f\u0330\bu\n\2\u0330\u00ea\3\2\2\2\u0331")
        buf.write("\u0332\7+\2\2\u0332\u0333\bv\13\2\u0333\u00ec\3\2\2\2")
        buf.write("\u0334\u0335\7=\2\2\u0335\u00ee\3\2\2\2\u0336\u0339\5")
        buf.write("\u00f1y\2\u0337\u0339\5\u00f3z\2\u0338\u0336\3\2\2\2\u0338")
        buf.write("\u0337\3\2\2\2\u0339\u00f0\3\2\2\2\u033a\u033f\7)\2\2")
        buf.write("\u033b\u033e\5\u00f9}\2\u033c\u033e\n\b\2\2\u033d\u033b")
        buf.write("\3\2\2\2\u033d\u033c\3\2\2\2\u033e\u0341\3\2\2\2\u033f")
        buf.write("\u033d\3\2\2\2\u033f\u0340\3\2\2\2\u0340\u0342\3\2\2\2")
        buf.write("\u0341\u033f\3\2\2\2\u0342\u034d\7)\2\2\u0343\u0348\7")
        buf.write("$\2\2\u0344\u0347\5\u00f9}\2\u0345\u0347\n\t\2\2\u0346")
        buf.write("\u0344\3\2\2\2\u0346\u0345\3\2\2\2\u0347\u034a\3\2\2\2")
        buf.write("\u0348\u0346\3\2\2\2\u0348\u0349\3\2\2\2\u0349\u034b\3")
        buf.write("\2\2\2\u034a\u0348\3\2\2\2\u034b\u034d\7$\2\2\u034c\u033a")
        buf.write("\3\2\2\2\u034c\u0343\3\2\2\2\u034d\u00f2\3\2\2\2\u034e")
        buf.write("\u034f\7)\2\2\u034f\u0350\7)\2\2\u0350\u0351\7)\2\2\u0351")
        buf.write("\u0355\3\2\2\2\u0352\u0354\5\u00f5{\2\u0353\u0352\3\2")
        buf.write("\2\2\u0354\u0357\3\2\2\2\u0355\u0356\3\2\2\2\u0355\u0353")
        buf.write("\3\2\2\2\u0356\u0358\3\2\2\2\u0357\u0355\3\2\2\2\u0358")
        buf.write("\u0359\7)\2\2\u0359\u035a\7)\2\2\u035a\u0369\7)\2\2\u035b")
        buf.write("\u035c\7$\2\2\u035c\u035d\7$\2\2\u035d\u035e\7$\2\2\u035e")
        buf.write("\u0362\3\2\2\2\u035f\u0361\5\u00f5{\2\u0360\u035f\3\2")
        buf.write("\2\2\u0361\u0364\3\2\2\2\u0362\u0363\3\2\2\2\u0362\u0360")
        buf.write("\3\2\2\2\u0363\u0365\3\2\2\2\u0364\u0362\3\2\2\2\u0365")
        buf.write("\u0366\7$\2\2\u0366\u0367\7$\2\2\u0367\u0369\7$\2\2\u0368")
        buf.write("\u034e\3\2\2\2\u0368\u035b\3\2\2\2\u0369\u00f4\3\2\2\2")
        buf.write("\u036a\u036d\5\u00f7|\2\u036b\u036d\5\u00f9}\2\u036c\u036a")
        buf.write("\3\2\2\2\u036c\u036b\3\2\2\2\u036d\u00f6\3\2\2\2\u036e")
        buf.write("\u036f\n\n\2\2\u036f\u00f8\3\2\2\2\u0370\u0371\7^\2\2")
        buf.write("\u0371\u0375\13\2\2\2\u0372\u0373\7^\2\2\u0373\u0375\5")
        buf.write("m\67\2\u0374\u0370\3\2\2\2\u0374\u0372\3\2\2\2\u0375\u00fa")
        buf.write("\3\2\2\2\36\2\u01ca\u01d0\u01d6\u01d9\u01e0\u01e5\u01ea")
        buf.write("\u01f2\u01fb\u01fe\u02f8\u0305\u030a\u0310\u0316\u031e")
        buf.write("\u0338\u033d\u033f\u0346\u0348\u034c\u0355\u0362\u0368")
        buf.write("\u036c\u0374\f\3\67\2\b\2\2\3e\3\3f\4\3q\5\3r\6\3s\7\3")
        buf.write("t\b\3u\t\3v\n")
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
    PASS = 80
    DEL = 81
    SPAWN = 82
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
    IN = 100
    COLON = 101
    NONE = 102
    ATOMICALLY = 103
    BOOL = 104
    ETERNAL = 105
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
            "'countLabel'", "'get_context'", "'contexts'", "'min'", "'max'", 
            "'len'", "'type'", "'str'", "'any'", "'all'", "'keys'", "'hash'", 
            "'choose'", "'end'", "'and='", "'or='", "'=>='", "'&='", "'|='", 
            "'^='", "'-='", "'+='", "'*='", "'/='", "'//='", "'%='", "'mod='", 
            "'**='", "'>>='", "'#'", "'(*'", "'*)'", "'!'", "'*'", "'as'", 
            "'.'", "'import'", "'print'", "'from'", "'..'", "'setintlevel'", 
            "'->'", "'save'", "'stop'", "'lambda'", "'?'", "'not'", "','", 
            "'const'", "'await'", "'assert'", "'var'", "'trap'", "'pass'", 
            "'del'", "'spawn'", "'invariant'", "'go'", "'builtin'", "'sequential'", 
            "'when'", "'let'", "'if'", "'elif'", "'else'", "'@'", "'while'", 
            "'def'", "'returns'", "'exists'", "'where'", "'='", "'for'", 
            "'in'", "':'", "'None'", "'atomically'", "'eternal'", "'['", 
            "']'", "'{'", "'}'", "'('", "')'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "NL", "WS", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
            "POINTER_OF", "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", 
            "RANGE", "SETINTLEVEL", "ARROW", "SAVE", "STOP", "LAMBDA", "ADDRESS_OF", 
            "NOT", "COMMA", "CONST", "AWAIT", "ASSERT", "VAR", "TRAP", "PASS", 
            "DEL", "SPAWN", "INVARIANT", "GO", "BUILTIN", "SEQUENTIAL", 
            "WHEN", "LET", "IF", "ELIF", "ELSE", "AT", "WHILE", "DEF", "RETURNS", 
            "EXISTS", "WHERE", "EQ", "FOR", "IN", "COLON", "NONE", "ATOMICALLY", 
            "BOOL", "ETERNAL", "INT", "NAME", "ATOM", "HEX_INTEGER", "OPEN_BRACK", 
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
                  "PASS", "DEL", "SPAWN", "INVARIANT", "GO", "BUILTIN", 
                  "SEQUENTIAL", "WHEN", "LET", "IF", "ELIF", "ELSE", "AT", 
                  "WHILE", "DEF", "RETURNS", "EXISTS", "WHERE", "EQ", "FOR", 
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
            actions[99] = self.FOR_action 
            actions[100] = self.IN_action 
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
     


