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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\177")
        buf.write("\u03cd\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("\4\u0084\t\u0084\4\u0085\t\u0085\3\2\3\2\3\2\3\2\3\3\3")
        buf.write("\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t")
        buf.write("\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\16")
        buf.write("\3\16\3\16\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\22\3\22\3\23\3\23\3\23\3\24\3\24\3\25\3\25\3\25\3\26")
        buf.write("\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3\32\3\32\3\32")
        buf.write("\3\32\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\35\3\35")
        buf.write("\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\37\3\37")
        buf.write("\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3 \3 ")
        buf.write("\3 \3 \3 \3 \3 \3 \3!\3!\3!\3!\3!\3!\3!\3!\3!\3!\3\"\3")
        buf.write("\"\3\"\3\"\3\"\3#\3#\3#\3#\3$\3$\3$\3$\3$\3%\3%\3%\3%")
        buf.write("\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3(\3(\3(\3(\3")
        buf.write("(\3)\3)\3)\3)\3*\3*\3*\3*\3*\3*\3*\3+\3+\3+\3+\3,\3,\3")
        buf.write(",\3,\3-\3-\3-\3-\3-\3.\3.\3.\3.\3/\3/\3/\3/\3/\3\60\3")
        buf.write("\60\3\60\3\60\3\61\3\61\3\61\3\61\3\62\3\62\3\62\3\63")
        buf.write("\3\63\3\63\3\64\3\64\3\64\3\65\3\65\3\65\3\66\3\66\3\66")
        buf.write("\3\67\3\67\3\67\38\38\38\39\39\39\39\3:\3:\3:\3;\3;\3")
        buf.write(";\3;\3;\3<\3<\3<\3<\3=\3=\3=\3=\3>\3>\3>\3>\3?\5?\u01fa")
        buf.write("\n?\3?\3?\7?\u01fe\n?\f?\16?\u0201\13?\3?\7?\u0204\n?")
        buf.write("\f?\16?\u0207\13?\5?\u0209\n?\3?\3?\3@\6@\u020e\n@\r@")
        buf.write("\16@\u020f\3@\6@\u0213\n@\r@\16@\u0214\3@\3@\3@\5@\u021a")
        buf.write("\n@\3@\3@\3A\3A\7A\u0220\nA\fA\16A\u0223\13A\3A\3A\3A")
        buf.write("\3A\7A\u0229\nA\fA\16A\u022c\13A\5A\u022e\nA\3B\3B\3C")
        buf.write("\3C\3C\3D\3D\3D\3E\3E\3F\3F\3F\3G\3G\3H\3H\3H\3H\3H\3")
        buf.write("H\3H\3I\3I\3I\3I\3I\3I\3J\3J\3J\3J\3J\3K\3K\3K\3L\3L\3")
        buf.write("L\3L\3L\3L\3L\3L\3L\3L\3L\3L\3M\3M\3M\3M\3M\3N\3N\3N\3")
        buf.write("N\3N\3O\3O\3O\3O\3O\3O\3O\3P\3P\3P\3P\3Q\3Q\3R\3R\3R\3")
        buf.write("R\3R\3R\3S\3S\3S\3S\3S\3S\3T\3T\3T\3T\3T\3T\3T\3U\3U\3")
        buf.write("U\3U\3V\3V\3V\3V\3V\3W\3W\3W\3W\3W\3X\3X\3X\3X\3Y\3Y\3")
        buf.write("Y\3Y\3Y\3Y\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3[\3[\3[\3[\3[\3[\3")
        buf.write("[\3[\3[\3[\3\\\3\\\3\\\3]\3]\3]\3]\3]\3]\3]\3]\3^\3^\3")
        buf.write("^\3^\3^\3^\3^\3^\3^\3^\3^\3_\3_\3_\3_\3_\3`\3`\3`\3`\3")
        buf.write("a\3a\3a\3b\3b\3b\3b\3b\3c\3c\3c\3c\3c\3d\3d\3e\3e\3e\3")
        buf.write("e\3e\3e\3f\3f\3f\3f\3f\3f\3f\3g\3g\3g\3g\3h\3h\3h\3h\3")
        buf.write("h\3h\3h\3h\3i\3i\3i\3i\3i\3i\3i\3j\3j\3j\3j\3j\3j\3k\3")
        buf.write("k\3l\3l\3l\3l\3l\3l\3m\3m\3m\3m\3m\3n\3n\3o\3o\3o\3o\3")
        buf.write("o\3p\3p\3p\3p\3p\3p\3p\3p\3p\3p\3p\3q\3q\3q\3q\3q\3q\3")
        buf.write("q\3q\3q\5q\u0330\nq\3r\3r\3r\3r\3r\3r\3r\3r\3s\6s\u033b")
        buf.write("\ns\rs\16s\u033c\3s\3s\3s\3s\6s\u0343\ns\rs\16s\u0344")
        buf.write("\3s\3s\3s\3s\6s\u034b\ns\rs\16s\u034c\3s\3s\3s\3s\6s\u0353")
        buf.write("\ns\rs\16s\u0354\5s\u0357\ns\3t\3t\7t\u035b\nt\ft\16t")
        buf.write("\u035e\13t\3u\3u\3u\5u\u0363\nu\3v\3v\3v\3v\7v\u0369\n")
        buf.write("v\fv\16v\u036c\13v\3v\3v\3w\3w\3w\3w\6w\u0374\nw\rw\16")
        buf.write("w\u0375\3x\3x\3y\3y\3y\3z\3z\3z\3{\3{\3{\3|\3|\3|\3}\3")
        buf.write("}\3}\3~\3~\3~\3\177\3\177\3\u0080\3\u0080\5\u0080\u0390")
        buf.write("\n\u0080\3\u0081\3\u0081\3\u0081\7\u0081\u0395\n\u0081")
        buf.write("\f\u0081\16\u0081\u0398\13\u0081\3\u0081\3\u0081\3\u0081")
        buf.write("\3\u0081\7\u0081\u039e\n\u0081\f\u0081\16\u0081\u03a1")
        buf.write("\13\u0081\3\u0081\5\u0081\u03a4\n\u0081\3\u0082\3\u0082")
        buf.write("\3\u0082\3\u0082\3\u0082\7\u0082\u03ab\n\u0082\f\u0082")
        buf.write("\16\u0082\u03ae\13\u0082\3\u0082\3\u0082\3\u0082\3\u0082")
        buf.write("\3\u0082\3\u0082\3\u0082\3\u0082\7\u0082\u03b8\n\u0082")
        buf.write("\f\u0082\16\u0082\u03bb\13\u0082\3\u0082\3\u0082\3\u0082")
        buf.write("\5\u0082\u03c0\n\u0082\3\u0083\3\u0083\5\u0083\u03c4\n")
        buf.write("\u0083\3\u0084\3\u0084\3\u0085\3\u0085\3\u0085\3\u0085")
        buf.write("\5\u0085\u03cc\n\u0085\5\u0221\u03ac\u03b9\2\u0086\3\3")
        buf.write("\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16")
        buf.write("\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61")
        buf.write("\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*")
        buf.write("S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q:s;u<w")
        buf.write("=y>{?}@\177A\u0081\2\u0083B\u0085C\u0087D\u0089E\u008b")
        buf.write("F\u008dG\u008fH\u0091I\u0093J\u0095K\u0097L\u0099M\u009b")
        buf.write("N\u009dO\u009fP\u00a1Q\u00a3R\u00a5S\u00a7T\u00a9U\u00ab")
        buf.write("V\u00adW\u00afX\u00b1Y\u00b3Z\u00b5[\u00b7\\\u00b9]\u00bb")
        buf.write("^\u00bd_\u00bf`\u00c1a\u00c3b\u00c5c\u00c7d\u00c9e\u00cb")
        buf.write("f\u00cdg\u00cfh\u00d1i\u00d3j\u00d5k\u00d7l\u00d9m\u00db")
        buf.write("n\u00ddo\u00dfp\u00e1q\u00e3r\u00e5s\u00e7t\u00e9u\u00eb")
        buf.write("v\u00edw\u00ef\2\u00f1x\u00f3y\u00f5z\u00f7{\u00f9|\u00fb")
        buf.write("}\u00fd~\u00ff\177\u0101\2\u0103\2\u0105\2\u0107\2\u0109")
        buf.write("\2\3\2\r\4\2\f\f\16\17\3\2\62;\5\2\62;CHch\3\2\62\63\3")
        buf.write("\2\629\5\2C\\aac|\6\2\62;C\\aac|\3\2\60\60\6\2\f\f\16")
        buf.write("\17))^^\6\2\f\f\16\17$$^^\3\2^^\2\u03e8\2\3\3\2\2\2\2")
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
        buf.write("\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3")
        buf.write("\2\2\2\2\177\3\2\2\2\2\u0083\3\2\2\2\2\u0085\3\2\2\2\2")
        buf.write("\u0087\3\2\2\2\2\u0089\3\2\2\2\2\u008b\3\2\2\2\2\u008d")
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
        buf.write("\3\2\2\2\2\u00e3\3\2\2\2\2\u00e5\3\2\2\2\2\u00e7\3\2\2")
        buf.write("\2\2\u00e9\3\2\2\2\2\u00eb\3\2\2\2\2\u00ed\3\2\2\2\2\u00f1")
        buf.write("\3\2\2\2\2\u00f3\3\2\2\2\2\u00f5\3\2\2\2\2\u00f7\3\2\2")
        buf.write("\2\2\u00f9\3\2\2\2\2\u00fb\3\2\2\2\2\u00fd\3\2\2\2\2\u00ff")
        buf.write("\3\2\2\2\3\u010b\3\2\2\2\5\u010f\3\2\2\2\7\u0112\3\2\2")
        buf.write("\2\t\u0114\3\2\2\2\13\u0116\3\2\2\2\r\u0118\3\2\2\2\17")
        buf.write("\u011a\3\2\2\2\21\u011c\3\2\2\2\23\u011f\3\2\2\2\25\u0121")
        buf.write("\3\2\2\2\27\u0123\3\2\2\2\31\u0127\3\2\2\2\33\u012a\3")
        buf.write("\2\2\2\35\u012d\3\2\2\2\37\u0130\3\2\2\2!\u0133\3\2\2")
        buf.write("\2#\u0136\3\2\2\2%\u0138\3\2\2\2\'\u013b\3\2\2\2)\u013d")
        buf.write("\3\2\2\2+\u0140\3\2\2\2-\u0143\3\2\2\2/\u0145\3\2\2\2")
        buf.write("\61\u0147\3\2\2\2\63\u0149\3\2\2\2\65\u014d\3\2\2\2\67")
        buf.write("\u0151\3\2\2\29\u0155\3\2\2\2;\u0159\3\2\2\2=\u0160\3")
        buf.write("\2\2\2?\u0169\3\2\2\2A\u0175\3\2\2\2C\u017f\3\2\2\2E\u0184")
        buf.write("\3\2\2\2G\u0188\3\2\2\2I\u018d\3\2\2\2K\u0191\3\2\2\2")
        buf.write("M\u0195\3\2\2\2O\u0199\3\2\2\2Q\u01a2\3\2\2\2S\u01a6\3")
        buf.write("\2\2\2U\u01ad\3\2\2\2W\u01b1\3\2\2\2Y\u01b5\3\2\2\2[\u01ba")
        buf.write("\3\2\2\2]\u01be\3\2\2\2_\u01c3\3\2\2\2a\u01c7\3\2\2\2")
        buf.write("c\u01cb\3\2\2\2e\u01ce\3\2\2\2g\u01d1\3\2\2\2i\u01d4\3")
        buf.write("\2\2\2k\u01d7\3\2\2\2m\u01da\3\2\2\2o\u01dd\3\2\2\2q\u01e0")
        buf.write("\3\2\2\2s\u01e4\3\2\2\2u\u01e7\3\2\2\2w\u01ec\3\2\2\2")
        buf.write("y\u01f0\3\2\2\2{\u01f4\3\2\2\2}\u01f9\3\2\2\2\177\u0219")
        buf.write("\3\2\2\2\u0081\u022d\3\2\2\2\u0083\u022f\3\2\2\2\u0085")
        buf.write("\u0231\3\2\2\2\u0087\u0234\3\2\2\2\u0089\u0237\3\2\2\2")
        buf.write("\u008b\u0239\3\2\2\2\u008d\u023c\3\2\2\2\u008f\u023e\3")
        buf.write("\2\2\2\u0091\u0245\3\2\2\2\u0093\u024b\3\2\2\2\u0095\u0250")
        buf.write("\3\2\2\2\u0097\u0253\3\2\2\2\u0099\u025f\3\2\2\2\u009b")
        buf.write("\u0264\3\2\2\2\u009d\u0269\3\2\2\2\u009f\u0270\3\2\2\2")
        buf.write("\u00a1\u0274\3\2\2\2\u00a3\u0276\3\2\2\2\u00a5\u027c\3")
        buf.write("\2\2\2\u00a7\u0282\3\2\2\2\u00a9\u0289\3\2\2\2\u00ab\u028d")
        buf.write("\3\2\2\2\u00ad\u0292\3\2\2\2\u00af\u0297\3\2\2\2\u00b1")
        buf.write("\u029b\3\2\2\2\u00b3\u02a1\3\2\2\2\u00b5\u02a9\3\2\2\2")
        buf.write("\u00b7\u02b3\3\2\2\2\u00b9\u02b6\3\2\2\2\u00bb\u02be\3")
        buf.write("\2\2\2\u00bd\u02c9\3\2\2\2\u00bf\u02ce\3\2\2\2\u00c1\u02d2")
        buf.write("\3\2\2\2\u00c3\u02d5\3\2\2\2\u00c5\u02da\3\2\2\2\u00c7")
        buf.write("\u02df\3\2\2\2\u00c9\u02e1\3\2\2\2\u00cb\u02e7\3\2\2\2")
        buf.write("\u00cd\u02ee\3\2\2\2\u00cf\u02f2\3\2\2\2\u00d1\u02fa\3")
        buf.write("\2\2\2\u00d3\u0301\3\2\2\2\u00d5\u0307\3\2\2\2\u00d7\u0309")
        buf.write("\3\2\2\2\u00d9\u030f\3\2\2\2\u00db\u0314\3\2\2\2\u00dd")
        buf.write("\u0316\3\2\2\2\u00df\u031b\3\2\2\2\u00e1\u032f\3\2\2\2")
        buf.write("\u00e3\u0331\3\2\2\2\u00e5\u0356\3\2\2\2\u00e7\u0358\3")
        buf.write("\2\2\2\u00e9\u035f\3\2\2\2\u00eb\u0364\3\2\2\2\u00ed\u036f")
        buf.write("\3\2\2\2\u00ef\u0377\3\2\2\2\u00f1\u0379\3\2\2\2\u00f3")
        buf.write("\u037c\3\2\2\2\u00f5\u037f\3\2\2\2\u00f7\u0382\3\2\2\2")
        buf.write("\u00f9\u0385\3\2\2\2\u00fb\u0388\3\2\2\2\u00fd\u038b\3")
        buf.write("\2\2\2\u00ff\u038f\3\2\2\2\u0101\u03a3\3\2\2\2\u0103\u03bf")
        buf.write("\3\2\2\2\u0105\u03c3\3\2\2\2\u0107\u03c5\3\2\2\2\u0109")
        buf.write("\u03cb\3\2\2\2\u010b\u010c\7c\2\2\u010c\u010d\7p\2\2\u010d")
        buf.write("\u010e\7f\2\2\u010e\4\3\2\2\2\u010f\u0110\7q\2\2\u0110")
        buf.write("\u0111\7t\2\2\u0111\6\3\2\2\2\u0112\u0113\7(\2\2\u0113")
        buf.write("\b\3\2\2\2\u0114\u0115\7~\2\2\u0115\n\3\2\2\2\u0116\u0117")
        buf.write("\7`\2\2\u0117\f\3\2\2\2\u0118\u0119\7/\2\2\u0119\16\3")
        buf.write("\2\2\2\u011a\u011b\7-\2\2\u011b\20\3\2\2\2\u011c\u011d")
        buf.write("\7\61\2\2\u011d\u011e\7\61\2\2\u011e\22\3\2\2\2\u011f")
        buf.write("\u0120\7\61\2\2\u0120\24\3\2\2\2\u0121\u0122\7\'\2\2\u0122")
        buf.write("\26\3\2\2\2\u0123\u0124\7o\2\2\u0124\u0125\7q\2\2\u0125")
        buf.write("\u0126\7f\2\2\u0126\30\3\2\2\2\u0127\u0128\7,\2\2\u0128")
        buf.write("\u0129\7,\2\2\u0129\32\3\2\2\2\u012a\u012b\7>\2\2\u012b")
        buf.write("\u012c\7>\2\2\u012c\34\3\2\2\2\u012d\u012e\7@\2\2\u012e")
        buf.write("\u012f\7@\2\2\u012f\36\3\2\2\2\u0130\u0131\7?\2\2\u0131")
        buf.write("\u0132\7?\2\2\u0132 \3\2\2\2\u0133\u0134\7#\2\2\u0134")
        buf.write("\u0135\7?\2\2\u0135\"\3\2\2\2\u0136\u0137\7>\2\2\u0137")
        buf.write("$\3\2\2\2\u0138\u0139\7>\2\2\u0139\u013a\7?\2\2\u013a")
        buf.write("&\3\2\2\2\u013b\u013c\7@\2\2\u013c(\3\2\2\2\u013d\u013e")
        buf.write("\7@\2\2\u013e\u013f\7?\2\2\u013f*\3\2\2\2\u0140\u0141")
        buf.write("\7?\2\2\u0141\u0142\7@\2\2\u0142,\3\2\2\2\u0143\u0144")
        buf.write("\7\u0080\2\2\u0144.\3\2\2\2\u0145\u0146\7A\2\2\u0146\60")
        buf.write("\3\2\2\2\u0147\u0148\7#\2\2\u0148\62\3\2\2\2\u0149\u014a")
        buf.write("\7c\2\2\u014a\u014b\7d\2\2\u014b\u014c\7u\2\2\u014c\64")
        buf.write("\3\2\2\2\u014d\u014e\7c\2\2\u014e\u014f\7n\2\2\u014f\u0150")
        buf.write("\7n\2\2\u0150\66\3\2\2\2\u0151\u0152\7c\2\2\u0152\u0153")
        buf.write("\7p\2\2\u0153\u0154\7{\2\2\u01548\3\2\2\2\u0155\u0156")
        buf.write("\7d\2\2\u0156\u0157\7k\2\2\u0157\u0158\7p\2\2\u0158:\3")
        buf.write("\2\2\2\u0159\u015a\7e\2\2\u015a\u015b\7j\2\2\u015b\u015c")
        buf.write("\7q\2\2\u015c\u015d\7q\2\2\u015d\u015e\7u\2\2\u015e\u015f")
        buf.write("\7g\2\2\u015f<\3\2\2\2\u0160\u0161\7e\2\2\u0161\u0162")
        buf.write("\7q\2\2\u0162\u0163\7p\2\2\u0163\u0164\7v\2\2\u0164\u0165")
        buf.write("\7g\2\2\u0165\u0166\7z\2\2\u0166\u0167\7v\2\2\u0167\u0168")
        buf.write("\7u\2\2\u0168>\3\2\2\2\u0169\u016a\7i\2\2\u016a\u016b")
        buf.write("\7g\2\2\u016b\u016c\7v\2\2\u016c\u016d\7a\2\2\u016d\u016e")
        buf.write("\7e\2\2\u016e\u016f\7q\2\2\u016f\u0170\7p\2\2\u0170\u0171")
        buf.write("\7v\2\2\u0171\u0172\7g\2\2\u0172\u0173\7z\2\2\u0173\u0174")
        buf.write("\7v\2\2\u0174@\3\2\2\2\u0175\u0176\7i\2\2\u0176\u0177")
        buf.write("\7g\2\2\u0177\u0178\7v\2\2\u0178\u0179\7a\2\2\u0179\u017a")
        buf.write("\7k\2\2\u017a\u017b\7f\2\2\u017b\u017c\7g\2\2\u017c\u017d")
        buf.write("\7p\2\2\u017d\u017e\7v\2\2\u017eB\3\2\2\2\u017f\u0180")
        buf.write("\7j\2\2\u0180\u0181\7c\2\2\u0181\u0182\7u\2\2\u0182\u0183")
        buf.write("\7j\2\2\u0183D\3\2\2\2\u0184\u0185\7j\2\2\u0185\u0186")
        buf.write("\7g\2\2\u0186\u0187\7z\2\2\u0187F\3\2\2\2\u0188\u0189")
        buf.write("\7m\2\2\u0189\u018a\7g\2\2\u018a\u018b\7{\2\2\u018b\u018c")
        buf.write("\7u\2\2\u018cH\3\2\2\2\u018d\u018e\7n\2\2\u018e\u018f")
        buf.write("\7g\2\2\u018f\u0190\7p\2\2\u0190J\3\2\2\2\u0191\u0192")
        buf.write("\7o\2\2\u0192\u0193\7c\2\2\u0193\u0194\7z\2\2\u0194L\3")
        buf.write("\2\2\2\u0195\u0196\7o\2\2\u0196\u0197\7k\2\2\u0197\u0198")
        buf.write("\7p\2\2\u0198N\3\2\2\2\u0199\u019a\7t\2\2\u019a\u019b")
        buf.write("\7g\2\2\u019b\u019c\7x\2\2\u019c\u019d\7g\2\2\u019d\u019e")
        buf.write("\7t\2\2\u019e\u019f\7u\2\2\u019f\u01a0\7g\2\2\u01a0\u01a1")
        buf.write("\7f\2\2\u01a1P\3\2\2\2\u01a2\u01a3\7u\2\2\u01a3\u01a4")
        buf.write("\7g\2\2\u01a4\u01a5\7v\2\2\u01a5R\3\2\2\2\u01a6\u01a7")
        buf.write("\7u\2\2\u01a7\u01a8\7q\2\2\u01a8\u01a9\7t\2\2\u01a9\u01aa")
        buf.write("\7v\2\2\u01aa\u01ab\7g\2\2\u01ab\u01ac\7f\2\2\u01acT\3")
        buf.write("\2\2\2\u01ad\u01ae\7u\2\2\u01ae\u01af\7v\2\2\u01af\u01b0")
        buf.write("\7t\2\2\u01b0V\3\2\2\2\u01b1\u01b2\7u\2\2\u01b2\u01b3")
        buf.write("\7w\2\2\u01b3\u01b4\7o\2\2\u01b4X\3\2\2\2\u01b5\u01b6")
        buf.write("\7v\2\2\u01b6\u01b7\7{\2\2\u01b7\u01b8\7r\2\2\u01b8\u01b9")
        buf.write("\7g\2\2\u01b9Z\3\2\2\2\u01ba\u01bb\7g\2\2\u01bb\u01bc")
        buf.write("\7p\2\2\u01bc\u01bd\7f\2\2\u01bd\\\3\2\2\2\u01be\u01bf")
        buf.write("\7c\2\2\u01bf\u01c0\7p\2\2\u01c0\u01c1\7f\2\2\u01c1\u01c2")
        buf.write("\7?\2\2\u01c2^\3\2\2\2\u01c3\u01c4\7q\2\2\u01c4\u01c5")
        buf.write("\7t\2\2\u01c5\u01c6\7?\2\2\u01c6`\3\2\2\2\u01c7\u01c8")
        buf.write("\7?\2\2\u01c8\u01c9\7@\2\2\u01c9\u01ca\7?\2\2\u01cab\3")
        buf.write("\2\2\2\u01cb\u01cc\7(\2\2\u01cc\u01cd\7?\2\2\u01cdd\3")
        buf.write("\2\2\2\u01ce\u01cf\7~\2\2\u01cf\u01d0\7?\2\2\u01d0f\3")
        buf.write("\2\2\2\u01d1\u01d2\7`\2\2\u01d2\u01d3\7?\2\2\u01d3h\3")
        buf.write("\2\2\2\u01d4\u01d5\7/\2\2\u01d5\u01d6\7?\2\2\u01d6j\3")
        buf.write("\2\2\2\u01d7\u01d8\7-\2\2\u01d8\u01d9\7?\2\2\u01d9l\3")
        buf.write("\2\2\2\u01da\u01db\7,\2\2\u01db\u01dc\7?\2\2\u01dcn\3")
        buf.write("\2\2\2\u01dd\u01de\7\61\2\2\u01de\u01df\7?\2\2\u01dfp")
        buf.write("\3\2\2\2\u01e0\u01e1\7\61\2\2\u01e1\u01e2\7\61\2\2\u01e2")
        buf.write("\u01e3\7?\2\2\u01e3r\3\2\2\2\u01e4\u01e5\7\'\2\2\u01e5")
        buf.write("\u01e6\7?\2\2\u01e6t\3\2\2\2\u01e7\u01e8\7o\2\2\u01e8")
        buf.write("\u01e9\7q\2\2\u01e9\u01ea\7f\2\2\u01ea\u01eb\7?\2\2\u01eb")
        buf.write("v\3\2\2\2\u01ec\u01ed\7,\2\2\u01ed\u01ee\7,\2\2\u01ee")
        buf.write("\u01ef\7?\2\2\u01efx\3\2\2\2\u01f0\u01f1\7@\2\2\u01f1")
        buf.write("\u01f2\7@\2\2\u01f2\u01f3\7?\2\2\u01f3z\3\2\2\2\u01f4")
        buf.write("\u01f5\7>\2\2\u01f5\u01f6\7>\2\2\u01f6\u01f7\7?\2\2\u01f7")
        buf.write("|\3\2\2\2\u01f8\u01fa\7\17\2\2\u01f9\u01f8\3\2\2\2\u01f9")
        buf.write("\u01fa\3\2\2\2\u01fa\u01fb\3\2\2\2\u01fb\u0208\7\f\2\2")
        buf.write("\u01fc\u01fe\7\"\2\2\u01fd\u01fc\3\2\2\2\u01fe\u0201\3")
        buf.write("\2\2\2\u01ff\u01fd\3\2\2\2\u01ff\u0200\3\2\2\2\u0200\u0209")
        buf.write("\3\2\2\2\u0201\u01ff\3\2\2\2\u0202\u0204\7\13\2\2\u0203")
        buf.write("\u0202\3\2\2\2\u0204\u0207\3\2\2\2\u0205\u0203\3\2\2\2")
        buf.write("\u0205\u0206\3\2\2\2\u0206\u0209\3\2\2\2\u0207\u0205\3")
        buf.write("\2\2\2\u0208\u01ff\3\2\2\2\u0208\u0205\3\2\2\2\u0209\u020a")
        buf.write("\3\2\2\2\u020a\u020b\b?\2\2\u020b~\3\2\2\2\u020c\u020e")
        buf.write("\7\"\2\2\u020d\u020c\3\2\2\2\u020e\u020f\3\2\2\2\u020f")
        buf.write("\u020d\3\2\2\2\u020f\u0210\3\2\2\2\u0210\u021a\3\2\2\2")
        buf.write("\u0211\u0213\7\13\2\2\u0212\u0211\3\2\2\2\u0213\u0214")
        buf.write("\3\2\2\2\u0214\u0212\3\2\2\2\u0214\u0215\3\2\2\2\u0215")
        buf.write("\u021a\3\2\2\2\u0216\u0217\7^\2\2\u0217\u021a\5}?\2\u0218")
        buf.write("\u021a\5\u0081A\2\u0219\u020d\3\2\2\2\u0219\u0212\3\2")
        buf.write("\2\2\u0219\u0216\3\2\2\2\u0219\u0218\3\2\2\2\u021a\u021b")
        buf.write("\3\2\2\2\u021b\u021c\b@\3\2\u021c\u0080\3\2\2\2\u021d")
        buf.write("\u0221\5\u0085C\2\u021e\u0220\13\2\2\2\u021f\u021e\3\2")
        buf.write("\2\2\u0220\u0223\3\2\2\2\u0221\u0222\3\2\2\2\u0221\u021f")
        buf.write("\3\2\2\2\u0222\u0224\3\2\2\2\u0223\u0221\3\2\2\2\u0224")
        buf.write("\u0225\5\u0087D\2\u0225\u022e\3\2\2\2\u0226\u022a\5\u0083")
        buf.write("B\2\u0227\u0229\n\2\2\2\u0228\u0227\3\2\2\2\u0229\u022c")
        buf.write("\3\2\2\2\u022a\u0228\3\2\2\2\u022a\u022b\3\2\2\2\u022b")
        buf.write("\u022e\3\2\2\2\u022c\u022a\3\2\2\2\u022d\u021d\3\2\2\2")
        buf.write("\u022d\u0226\3\2\2\2\u022e\u0082\3\2\2\2\u022f\u0230\7")
        buf.write("%\2\2\u0230\u0084\3\2\2\2\u0231\u0232\7*\2\2\u0232\u0233")
        buf.write("\7,\2\2\u0233\u0086\3\2\2\2\u0234\u0235\7,\2\2\u0235\u0236")
        buf.write("\7+\2\2\u0236\u0088\3\2\2\2\u0237\u0238\7,\2\2\u0238\u008a")
        buf.write("\3\2\2\2\u0239\u023a\7c\2\2\u023a\u023b\7u\2\2\u023b\u008c")
        buf.write("\3\2\2\2\u023c\u023d\7\60\2\2\u023d\u008e\3\2\2\2\u023e")
        buf.write("\u023f\7k\2\2\u023f\u0240\7o\2\2\u0240\u0241\7r\2\2\u0241")
        buf.write("\u0242\7q\2\2\u0242\u0243\7t\2\2\u0243\u0244\7v\2\2\u0244")
        buf.write("\u0090\3\2\2\2\u0245\u0246\7r\2\2\u0246\u0247\7t\2\2\u0247")
        buf.write("\u0248\7k\2\2\u0248\u0249\7p\2\2\u0249\u024a\7v\2\2\u024a")
        buf.write("\u0092\3\2\2\2\u024b\u024c\7h\2\2\u024c\u024d\7t\2\2\u024d")
        buf.write("\u024e\7q\2\2\u024e\u024f\7o\2\2\u024f\u0094\3\2\2\2\u0250")
        buf.write("\u0251\7\60\2\2\u0251\u0252\7\60\2\2\u0252\u0096\3\2\2")
        buf.write("\2\u0253\u0254\7u\2\2\u0254\u0255\7g\2\2\u0255\u0256\7")
        buf.write("v\2\2\u0256\u0257\7k\2\2\u0257\u0258\7p\2\2\u0258\u0259")
        buf.write("\7v\2\2\u0259\u025a\7n\2\2\u025a\u025b\7g\2\2\u025b\u025c")
        buf.write("\7x\2\2\u025c\u025d\7g\2\2\u025d\u025e\7n\2\2\u025e\u0098")
        buf.write("\3\2\2\2\u025f\u0260\7u\2\2\u0260\u0261\7c\2\2\u0261\u0262")
        buf.write("\7x\2\2\u0262\u0263\7g\2\2\u0263\u009a\3\2\2\2\u0264\u0265")
        buf.write("\7u\2\2\u0265\u0266\7v\2\2\u0266\u0267\7q\2\2\u0267\u0268")
        buf.write("\7r\2\2\u0268\u009c\3\2\2\2\u0269\u026a\7n\2\2\u026a\u026b")
        buf.write("\7c\2\2\u026b\u026c\7o\2\2\u026c\u026d\7d\2\2\u026d\u026e")
        buf.write("\7f\2\2\u026e\u026f\7c\2\2\u026f\u009e\3\2\2\2\u0270\u0271")
        buf.write("\7p\2\2\u0271\u0272\7q\2\2\u0272\u0273\7v\2\2\u0273\u00a0")
        buf.write("\3\2\2\2\u0274\u0275\7.\2\2\u0275\u00a2\3\2\2\2\u0276")
        buf.write("\u0277\7e\2\2\u0277\u0278\7q\2\2\u0278\u0279\7p\2\2\u0279")
        buf.write("\u027a\7u\2\2\u027a\u027b\7v\2\2\u027b\u00a4\3\2\2\2\u027c")
        buf.write("\u027d\7c\2\2\u027d\u027e\7y\2\2\u027e\u027f\7c\2\2\u027f")
        buf.write("\u0280\7k\2\2\u0280\u0281\7v\2\2\u0281\u00a6\3\2\2\2\u0282")
        buf.write("\u0283\7c\2\2\u0283\u0284\7u\2\2\u0284\u0285\7u\2\2\u0285")
        buf.write("\u0286\7g\2\2\u0286\u0287\7t\2\2\u0287\u0288\7v\2\2\u0288")
        buf.write("\u00a8\3\2\2\2\u0289\u028a\7x\2\2\u028a\u028b\7c\2\2\u028b")
        buf.write("\u028c\7t\2\2\u028c\u00aa\3\2\2\2\u028d\u028e\7v\2\2\u028e")
        buf.write("\u028f\7t\2\2\u028f\u0290\7c\2\2\u0290\u0291\7r\2\2\u0291")
        buf.write("\u00ac\3\2\2\2\u0292\u0293\7r\2\2\u0293\u0294\7c\2\2\u0294")
        buf.write("\u0295\7u\2\2\u0295\u0296\7u\2\2\u0296\u00ae\3\2\2\2\u0297")
        buf.write("\u0298\7f\2\2\u0298\u0299\7g\2\2\u0299\u029a\7n\2\2\u029a")
        buf.write("\u00b0\3\2\2\2\u029b\u029c\7u\2\2\u029c\u029d\7r\2\2\u029d")
        buf.write("\u029e\7c\2\2\u029e\u029f\7y\2\2\u029f\u02a0\7p\2\2\u02a0")
        buf.write("\u00b2\3\2\2\2\u02a1\u02a2\7h\2\2\u02a2\u02a3\7k\2\2\u02a3")
        buf.write("\u02a4\7p\2\2\u02a4\u02a5\7c\2\2\u02a5\u02a6\7n\2\2\u02a6")
        buf.write("\u02a7\7n\2\2\u02a7\u02a8\7{\2\2\u02a8\u00b4\3\2\2\2\u02a9")
        buf.write("\u02aa\7k\2\2\u02aa\u02ab\7p\2\2\u02ab\u02ac\7x\2\2\u02ac")
        buf.write("\u02ad\7c\2\2\u02ad\u02ae\7t\2\2\u02ae\u02af\7k\2\2\u02af")
        buf.write("\u02b0\7c\2\2\u02b0\u02b1\7p\2\2\u02b1\u02b2\7v\2\2\u02b2")
        buf.write("\u00b6\3\2\2\2\u02b3\u02b4\7i\2\2\u02b4\u02b5\7q\2\2\u02b5")
        buf.write("\u00b8\3\2\2\2\u02b6\u02b7\7d\2\2\u02b7\u02b8\7w\2\2\u02b8")
        buf.write("\u02b9\7k\2\2\u02b9\u02ba\7n\2\2\u02ba\u02bb\7v\2\2\u02bb")
        buf.write("\u02bc\7k\2\2\u02bc\u02bd\7p\2\2\u02bd\u00ba\3\2\2\2\u02be")
        buf.write("\u02bf\7u\2\2\u02bf\u02c0\7g\2\2\u02c0\u02c1\7s\2\2\u02c1")
        buf.write("\u02c2\7w\2\2\u02c2\u02c3\7g\2\2\u02c3\u02c4\7p\2\2\u02c4")
        buf.write("\u02c5\7v\2\2\u02c5\u02c6\7k\2\2\u02c6\u02c7\7c\2\2\u02c7")
        buf.write("\u02c8\7n\2\2\u02c8\u00bc\3\2\2\2\u02c9\u02ca\7y\2\2\u02ca")
        buf.write("\u02cb\7j\2\2\u02cb\u02cc\7g\2\2\u02cc\u02cd\7p\2\2\u02cd")
        buf.write("\u00be\3\2\2\2\u02ce\u02cf\7n\2\2\u02cf\u02d0\7g\2\2\u02d0")
        buf.write("\u02d1\7v\2\2\u02d1\u00c0\3\2\2\2\u02d2\u02d3\7k\2\2\u02d3")
        buf.write("\u02d4\7h\2\2\u02d4\u00c2\3\2\2\2\u02d5\u02d6\7g\2\2\u02d6")
        buf.write("\u02d7\7n\2\2\u02d7\u02d8\7k\2\2\u02d8\u02d9\7h\2\2\u02d9")
        buf.write("\u00c4\3\2\2\2\u02da\u02db\7g\2\2\u02db\u02dc\7n\2\2\u02dc")
        buf.write("\u02dd\7u\2\2\u02dd\u02de\7g\2\2\u02de\u00c6\3\2\2\2\u02df")
        buf.write("\u02e0\7B\2\2\u02e0\u00c8\3\2\2\2\u02e1\u02e2\7y\2\2\u02e2")
        buf.write("\u02e3\7j\2\2\u02e3\u02e4\7k\2\2\u02e4\u02e5\7n\2\2\u02e5")
        buf.write("\u02e6\7g\2\2\u02e6\u00ca\3\2\2\2\u02e7\u02e8\7i\2\2\u02e8")
        buf.write("\u02e9\7n\2\2\u02e9\u02ea\7q\2\2\u02ea\u02eb\7d\2\2\u02eb")
        buf.write("\u02ec\7c\2\2\u02ec\u02ed\7n\2\2\u02ed\u00cc\3\2\2\2\u02ee")
        buf.write("\u02ef\7f\2\2\u02ef\u02f0\7g\2\2\u02f0\u02f1\7h\2\2\u02f1")
        buf.write("\u00ce\3\2\2\2\u02f2\u02f3\7t\2\2\u02f3\u02f4\7g\2\2\u02f4")
        buf.write("\u02f5\7v\2\2\u02f5\u02f6\7w\2\2\u02f6\u02f7\7t\2\2\u02f7")
        buf.write("\u02f8\7p\2\2\u02f8\u02f9\7u\2\2\u02f9\u00d0\3\2\2\2\u02fa")
        buf.write("\u02fb\7g\2\2\u02fb\u02fc\7z\2\2\u02fc\u02fd\7k\2\2\u02fd")
        buf.write("\u02fe\7u\2\2\u02fe\u02ff\7v\2\2\u02ff\u0300\7u\2\2\u0300")
        buf.write("\u00d2\3\2\2\2\u0301\u0302\7y\2\2\u0302\u0303\7j\2\2\u0303")
        buf.write("\u0304\7g\2\2\u0304\u0305\7t\2\2\u0305\u0306\7g\2\2\u0306")
        buf.write("\u00d4\3\2\2\2\u0307\u0308\7?\2\2\u0308\u00d6\3\2\2\2")
        buf.write("\u0309\u030a\7h\2\2\u030a\u030b\7q\2\2\u030b\u030c\7t")
        buf.write("\2\2\u030c\u030d\3\2\2\2\u030d\u030e\bl\4\2\u030e\u00d8")
        buf.write("\3\2\2\2\u030f\u0310\7k\2\2\u0310\u0311\7p\2\2\u0311\u0312")
        buf.write("\3\2\2\2\u0312\u0313\bm\5\2\u0313\u00da\3\2\2\2\u0314")
        buf.write("\u0315\7<\2\2\u0315\u00dc\3\2\2\2\u0316\u0317\7P\2\2\u0317")
        buf.write("\u0318\7q\2\2\u0318\u0319\7p\2\2\u0319\u031a\7g\2\2\u031a")
        buf.write("\u00de\3\2\2\2\u031b\u031c\7c\2\2\u031c\u031d\7v\2\2\u031d")
        buf.write("\u031e\7q\2\2\u031e\u031f\7o\2\2\u031f\u0320\7k\2\2\u0320")
        buf.write("\u0321\7e\2\2\u0321\u0322\7c\2\2\u0322\u0323\7n\2\2\u0323")
        buf.write("\u0324\7n\2\2\u0324\u0325\7{\2\2\u0325\u00e0\3\2\2\2\u0326")
        buf.write("\u0327\7H\2\2\u0327\u0328\7c\2\2\u0328\u0329\7n\2\2\u0329")
        buf.write("\u032a\7u\2\2\u032a\u0330\7g\2\2\u032b\u032c\7V\2\2\u032c")
        buf.write("\u032d\7t\2\2\u032d\u032e\7w\2\2\u032e\u0330\7g\2\2\u032f")
        buf.write("\u0326\3\2\2\2\u032f\u032b\3\2\2\2\u0330\u00e2\3\2\2\2")
        buf.write("\u0331\u0332\7g\2\2\u0332\u0333\7v\2\2\u0333\u0334\7g")
        buf.write("\2\2\u0334\u0335\7t\2\2\u0335\u0336\7p\2\2\u0336\u0337")
        buf.write("\7c\2\2\u0337\u0338\7n\2\2\u0338\u00e4\3\2\2\2\u0339\u033b")
        buf.write("\t\3\2\2\u033a\u0339\3\2\2\2\u033b\u033c\3\2\2\2\u033c")
        buf.write("\u033a\3\2\2\2\u033c\u033d\3\2\2\2\u033d\u0357\3\2\2\2")
        buf.write("\u033e\u033f\7\62\2\2\u033f\u0340\7z\2\2\u0340\u0342\3")
        buf.write("\2\2\2\u0341\u0343\t\4\2\2\u0342\u0341\3\2\2\2\u0343\u0344")
        buf.write("\3\2\2\2\u0344\u0342\3\2\2\2\u0344\u0345\3\2\2\2\u0345")
        buf.write("\u0357\3\2\2\2\u0346\u0347\7\62\2\2\u0347\u0348\7d\2\2")
        buf.write("\u0348\u034a\3\2\2\2\u0349\u034b\t\5\2\2\u034a\u0349\3")
        buf.write("\2\2\2\u034b\u034c\3\2\2\2\u034c\u034a\3\2\2\2\u034c\u034d")
        buf.write("\3\2\2\2\u034d\u0357\3\2\2\2\u034e\u034f\7\62\2\2\u034f")
        buf.write("\u0350\7q\2\2\u0350\u0352\3\2\2\2\u0351\u0353\t\6\2\2")
        buf.write("\u0352\u0351\3\2\2\2\u0353\u0354\3\2\2\2\u0354\u0352\3")
        buf.write("\2\2\2\u0354\u0355\3\2\2\2\u0355\u0357\3\2\2\2\u0356\u033a")
        buf.write("\3\2\2\2\u0356\u033e\3\2\2\2\u0356\u0346\3\2\2\2\u0356")
        buf.write("\u034e\3\2\2\2\u0357\u00e6\3\2\2\2\u0358\u035c\t\7\2\2")
        buf.write("\u0359\u035b\t\b\2\2\u035a\u0359\3\2\2\2\u035b\u035e\3")
        buf.write("\2\2\2\u035c\u035a\3\2\2\2\u035c\u035d\3\2\2\2\u035d\u00e8")
        buf.write("\3\2\2\2\u035e\u035c\3\2\2\2\u035f\u0362\t\t\2\2\u0360")
        buf.write("\u0363\5\u00edw\2\u0361\u0363\5\u00e7t\2\u0362\u0360\3")
        buf.write("\2\2\2\u0362\u0361\3\2\2\2\u0363\u00ea\3\2\2\2\u0364\u0365")
        buf.write("\7/\2\2\u0365\u0366\7@\2\2\u0366\u036a\3\2\2\2\u0367\u0369")
        buf.write("\7\"\2\2\u0368\u0367\3\2\2\2\u0369\u036c\3\2\2\2\u036a")
        buf.write("\u0368\3\2\2\2\u036a\u036b\3\2\2\2\u036b\u036d\3\2\2\2")
        buf.write("\u036c\u036a\3\2\2\2\u036d\u036e\5\u00e7t\2\u036e\u00ec")
        buf.write("\3\2\2\2\u036f\u0370\7\62\2\2\u0370\u0371\7Z\2\2\u0371")
        buf.write("\u0373\3\2\2\2\u0372\u0374\5\u00efx\2\u0373\u0372\3\2")
        buf.write("\2\2\u0374\u0375\3\2\2\2\u0375\u0373\3\2\2\2\u0375\u0376")
        buf.write("\3\2\2\2\u0376\u00ee\3\2\2\2\u0377\u0378\t\4\2\2\u0378")
        buf.write("\u00f0\3\2\2\2\u0379\u037a\7]\2\2\u037a\u037b\by\6\2\u037b")
        buf.write("\u00f2\3\2\2\2\u037c\u037d\7_\2\2\u037d\u037e\bz\7\2\u037e")
        buf.write("\u00f4\3\2\2\2\u037f\u0380\7}\2\2\u0380\u0381\b{\b\2\u0381")
        buf.write("\u00f6\3\2\2\2\u0382\u0383\7\177\2\2\u0383\u0384\b|\t")
        buf.write("\2\u0384\u00f8\3\2\2\2\u0385\u0386\7*\2\2\u0386\u0387")
        buf.write("\b}\n\2\u0387\u00fa\3\2\2\2\u0388\u0389\7+\2\2\u0389\u038a")
        buf.write("\b~\13\2\u038a\u00fc\3\2\2\2\u038b\u038c\7=\2\2\u038c")
        buf.write("\u00fe\3\2\2\2\u038d\u0390\5\u0101\u0081\2\u038e\u0390")
        buf.write("\5\u0103\u0082\2\u038f\u038d\3\2\2\2\u038f\u038e\3\2\2")
        buf.write("\2\u0390\u0100\3\2\2\2\u0391\u0396\7)\2\2\u0392\u0395")
        buf.write("\5\u0109\u0085\2\u0393\u0395\n\n\2\2\u0394\u0392\3\2\2")
        buf.write("\2\u0394\u0393\3\2\2\2\u0395\u0398\3\2\2\2\u0396\u0394")
        buf.write("\3\2\2\2\u0396\u0397\3\2\2\2\u0397\u0399\3\2\2\2\u0398")
        buf.write("\u0396\3\2\2\2\u0399\u03a4\7)\2\2\u039a\u039f\7$\2\2\u039b")
        buf.write("\u039e\5\u0109\u0085\2\u039c\u039e\n\13\2\2\u039d\u039b")
        buf.write("\3\2\2\2\u039d\u039c\3\2\2\2\u039e\u03a1\3\2\2\2\u039f")
        buf.write("\u039d\3\2\2\2\u039f\u03a0\3\2\2\2\u03a0\u03a2\3\2\2\2")
        buf.write("\u03a1\u039f\3\2\2\2\u03a2\u03a4\7$\2\2\u03a3\u0391\3")
        buf.write("\2\2\2\u03a3\u039a\3\2\2\2\u03a4\u0102\3\2\2\2\u03a5\u03a6")
        buf.write("\7)\2\2\u03a6\u03a7\7)\2\2\u03a7\u03a8\7)\2\2\u03a8\u03ac")
        buf.write("\3\2\2\2\u03a9\u03ab\5\u0105\u0083\2\u03aa\u03a9\3\2\2")
        buf.write("\2\u03ab\u03ae\3\2\2\2\u03ac\u03ad\3\2\2\2\u03ac\u03aa")
        buf.write("\3\2\2\2\u03ad\u03af\3\2\2\2\u03ae\u03ac\3\2\2\2\u03af")
        buf.write("\u03b0\7)\2\2\u03b0\u03b1\7)\2\2\u03b1\u03c0\7)\2\2\u03b2")
        buf.write("\u03b3\7$\2\2\u03b3\u03b4\7$\2\2\u03b4\u03b5\7$\2\2\u03b5")
        buf.write("\u03b9\3\2\2\2\u03b6\u03b8\5\u0105\u0083\2\u03b7\u03b6")
        buf.write("\3\2\2\2\u03b8\u03bb\3\2\2\2\u03b9\u03ba\3\2\2\2\u03b9")
        buf.write("\u03b7\3\2\2\2\u03ba\u03bc\3\2\2\2\u03bb\u03b9\3\2\2\2")
        buf.write("\u03bc\u03bd\7$\2\2\u03bd\u03be\7$\2\2\u03be\u03c0\7$")
        buf.write("\2\2\u03bf\u03a5\3\2\2\2\u03bf\u03b2\3\2\2\2\u03c0\u0104")
        buf.write("\3\2\2\2\u03c1\u03c4\5\u0107\u0084\2\u03c2\u03c4\5\u0109")
        buf.write("\u0085\2\u03c3\u03c1\3\2\2\2\u03c3\u03c2\3\2\2\2\u03c4")
        buf.write("\u0106\3\2\2\2\u03c5\u03c6\n\f\2\2\u03c6\u0108\3\2\2\2")
        buf.write("\u03c7\u03c8\7^\2\2\u03c8\u03cc\13\2\2\2\u03c9\u03ca\7")
        buf.write("^\2\2\u03ca\u03cc\5}?\2\u03cb\u03c7\3\2\2\2\u03cb\u03c9")
        buf.write("\3\2\2\2\u03cc\u010a\3\2\2\2\"\2\u01f9\u01ff\u0205\u0208")
        buf.write("\u020f\u0214\u0219\u0221\u022a\u022d\u032f\u033c\u0344")
        buf.write("\u034c\u0354\u0356\u035c\u0362\u036a\u0375\u038f\u0394")
        buf.write("\u0396\u039d\u039f\u03a3\u03ac\u03b9\u03bf\u03c3\u03cb")
        buf.write("\f\3?\2\b\2\2\3l\3\3m\4\3y\5\3z\6\3{\7\3|\b\3}\t\3~\n")
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
    NL = 62
    WS = 63
    COMMENT_START = 64
    OPEN_MULTI_COMMENT = 65
    CLOSE_MULTI_COMMENT = 66
    STAR = 67
    AS = 68
    DOT = 69
    IMPORT = 70
    PRINT = 71
    FROM = 72
    RANGE = 73
    SETINTLEVEL = 74
    SAVE = 75
    STOP = 76
    LAMBDA = 77
    NOT = 78
    COMMA = 79
    CONST = 80
    AWAIT = 81
    ASSERT = 82
    VAR = 83
    TRAP = 84
    PASS = 85
    DEL = 86
    SPAWN = 87
    FINALLY = 88
    INVARIANT = 89
    GO = 90
    BUILTIN = 91
    SEQUENTIAL = 92
    WHEN = 93
    LET = 94
    IF = 95
    ELIF = 96
    ELSE = 97
    AT = 98
    WHILE = 99
    GLOBAL = 100
    DEF = 101
    RETURNS = 102
    EXISTS = 103
    WHERE = 104
    EQ = 105
    FOR = 106
    IN = 107
    COLON = 108
    NONE = 109
    ATOMICALLY = 110
    BOOL = 111
    ETERNAL = 112
    INT = 113
    NAME = 114
    ATOM = 115
    ARROWID = 116
    HEX_INTEGER = 117
    OPEN_BRACK = 118
    CLOSE_BRACK = 119
    OPEN_BRACES = 120
    CLOSE_BRACES = 121
    OPEN_PAREN = 122
    CLOSE_PAREN = 123
    SEMI_COLON = 124
    STRING = 125

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'or'", "'&'", "'|'", "'^'", "'-'", "'+'", "'//'", 
            "'/'", "'%'", "'mod'", "'**'", "'<<'", "'>>'", "'=='", "'!='", 
            "'<'", "'<='", "'>'", "'>='", "'=>'", "'~'", "'?'", "'!'", "'abs'", 
            "'all'", "'any'", "'bin'", "'choose'", "'contexts'", "'get_context'", 
            "'get_ident'", "'hash'", "'hex'", "'keys'", "'len'", "'max'", 
            "'min'", "'reversed'", "'set'", "'sorted'", "'str'", "'sum'", 
            "'type'", "'end'", "'and='", "'or='", "'=>='", "'&='", "'|='", 
            "'^='", "'-='", "'+='", "'*='", "'/='", "'//='", "'%='", "'mod='", 
            "'**='", "'>>='", "'<<='", "'#'", "'(*'", "'*)'", "'*'", "'as'", 
            "'.'", "'import'", "'print'", "'from'", "'..'", "'setintlevel'", 
            "'save'", "'stop'", "'lambda'", "'not'", "','", "'const'", "'await'", 
            "'assert'", "'var'", "'trap'", "'pass'", "'del'", "'spawn'", 
            "'finally'", "'invariant'", "'go'", "'builtin'", "'sequential'", 
            "'when'", "'let'", "'if'", "'elif'", "'else'", "'@'", "'while'", 
            "'global'", "'def'", "'returns'", "'exists'", "'where'", "'='", 
            "'for'", "'in'", "':'", "'None'", "'atomically'", "'eternal'", 
            "'['", "']'", "'{'", "'}'", "'('", "')'", "';'" ]

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
                  "T__56", "T__57", "T__58", "T__59", "T__60", "NL", "WS", 
                  "COMMENT", "COMMENT_START", "OPEN_MULTI_COMMENT", "CLOSE_MULTI_COMMENT", 
                  "STAR", "AS", "DOT", "IMPORT", "PRINT", "FROM", "RANGE", 
                  "SETINTLEVEL", "SAVE", "STOP", "LAMBDA", "NOT", "COMMA", 
                  "CONST", "AWAIT", "ASSERT", "VAR", "TRAP", "PASS", "DEL", 
                  "SPAWN", "FINALLY", "INVARIANT", "GO", "BUILTIN", "SEQUENTIAL", 
                  "WHEN", "LET", "IF", "ELIF", "ELSE", "AT", "WHILE", "GLOBAL", 
                  "DEF", "RETURNS", "EXISTS", "WHERE", "EQ", "FOR", "IN", 
                  "COLON", "NONE", "ATOMICALLY", "BOOL", "ETERNAL", "INT", 
                  "NAME", "ATOM", "ARROWID", "HEX_INTEGER", "HEX_DIGIT", 
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
            actions[61] = self.NL_action 
            actions[106] = self.FOR_action 
            actions[107] = self.IN_action 
            actions[119] = self.OPEN_BRACK_action 
            actions[120] = self.CLOSE_BRACK_action 
            actions[121] = self.OPEN_BRACES_action 
            actions[122] = self.CLOSE_BRACES_action 
            actions[123] = self.OPEN_PAREN_action 
            actions[124] = self.CLOSE_PAREN_action 
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
     


