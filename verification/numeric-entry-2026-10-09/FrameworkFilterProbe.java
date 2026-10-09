/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
import android.text.SpannedString;
import android.text.method.DigitsKeyListener;
import java.nio.file.Path;
import java.text.DecimalFormatSymbols;
import java.text.NumberFormat;
import java.text.ParsePosition;
import java.util.Locale;
import javax.xml.parsers.DocumentBuilderFactory;

/** Direct unchanged Android key-filter bytecode on a host JVM, not an Android runtime.
 * Single-character insertion avoids Android VM-only array operations. No shims are used.
 * Locale symbols/parsing are the host JDK's. App-level tests run separately in Robolectric.
 */
public class FrameworkFilterProbe {
    static String insert(DigitsKeyListener listener, String text) {
        String result="";
        for(int i=0;i<text.length();i++) {
            String next=text.substring(i,i+1);
            var filtered=listener.filter(next,0,1,new SpannedString(result),result.length(),result.length());
            result+=(filtered==null ? next : filtered.toString());
        }
        return result;
    }
    static String accepted(DecimalFormatSymbols s) {
        String digits="";
        for(int i=0;i<10;i++) digits+=(char)(s.getZeroDigit()+i);
        return "0123456789.+-"+digits+s.getDecimalSeparator()+s.getMinusSign();
    }
    static Double parse(String text, Locale locale) {
        try {double n=Double.parseDouble(text);return Double.isFinite(n)?n:null;} catch(NumberFormatException ignored) {}
        var p=new ParsePosition(0);
        var n=NumberFormat.getNumberInstance(locale).parse(text,p);
        return n!=null && p.getIndex()==text.length() && Double.isFinite(n.doubleValue()) ? n.doubleValue() : null;
    }
    static void require(boolean yes,String message) {if(!yes)throw new AssertionError(message);}
    public static void main(String[] args) throws Exception {
        var nodes=DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(Path.of(args[0]).toFile()).getElementsByTagName("item");
        int preserved=0, affectedInteger=0, affectedDecimal=0;
        System.out.println("tag\tzero_digit\tdecimal_separator\tlegacy_integer\tlegacy_decimal\tfixed_integer\tfixed_decimal");
        for(int i=0;i<nodes.getLength();i++) {
            String tag=nodes.item(i).getTextContent().trim();var locale=Locale.forLanguageTag(tag);
            var symbols=DecimalFormatSymbols.getInstance(locale);
            String integer="", decimal="";
            for(char n:"125".toCharArray()) integer+=(char)(symbols.getZeroDigit()+n-'0');
            decimal=integer.substring(0,2)+symbols.getDecimalSeparator()+integer.substring(2);
            String oldInteger=insert(DigitsKeyListener.getInstance(false,false),integer);
            String oldDecimal=insert(DigitsKeyListener.getInstance(false,true),decimal);
            String fixedInteger=insert(DigitsKeyListener.getInstance(accepted(symbols)),integer);
            String fixedDecimal=insert(DigitsKeyListener.getInstance(accepted(symbols)),decimal);
            require(integer.equals(fixedInteger),tag+" integer changed");
            require(decimal.equals(fixedDecimal),tag+" decimal changed");
            require(Double.valueOf(125).equals(parse(fixedInteger,locale)),tag+" integer parse");
            require(Double.valueOf(12.5).equals(parse(fixedDecimal,locale)),tag+" decimal parse");
            require("12.5".equals(insert(DigitsKeyListener.getInstance(accepted(symbols)),"12.5")),tag+" ASCII dot changed");
            String negative="-"+integer;
            require(negative.equals(insert(DigitsKeyListener.getInstance(accepted(symbols)),negative)),tag+" sign changed");
            var parsed=parse(negative,locale);require(parsed==null || parsed<0,tag+" became positive");
            preserved++;
            if(!integer.equals(oldInteger)) affectedInteger++;
            if(!decimal.equals(oldDecimal)) affectedDecimal++;
            System.out.println(tag+"\tU+"+String.format("%04X",(int)symbols.getZeroDigit())+"\tU+"+String.format("%04X",(int)symbols.getDecimalSeparator())+"\t"+oldInteger+"\t"+oldDecimal+"\t"+fixedInteger+"\t"+fixedDecimal);
        }
        System.err.println("locales="+preserved+" changed_legacy_integer="+affectedInteger+" changed_legacy_decimal="+affectedDecimal+" candidate_preservation_and_parse=PASS");
    }
}
