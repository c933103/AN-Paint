import java.text.NumberFormat;
import java.text.ParsePosition;
import java.util.Locale;
class SwedishNumberProbe {
  public static void main(String[] args) {
    for (String tag : new String[]{"en-US", "sv"}) {
      ParsePosition position = new ParsePosition(0);
      Number number = NumberFormat.getNumberInstance(Locale.forLanguageTag(tag)).parse("1,5", position);
      System.out.println(tag + ": text=1,5 parsed=" + number + " consumed=" + position.getIndex());
    }
  }
}
