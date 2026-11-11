import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class FormattingCheck {
  static String decode(String x) {
    return new String(Base64.getDecoder().decode(x), StandardCharsets.UTF_8);
  }
  public static void main(String[] args) throws Exception {
    int count = 0;
    for (String row : Files.readAllLines(Path.of(args[0]), StandardCharsets.UTF_8)) {
      String[] p = row.split("\\t", -1);
      Object[] values = new Object[p.length - 4];
      for (int n = 4; n < p.length; n++) {
        values[n - 4] = p[n].startsWith("d:") ? Integer.parseInt(p[n].substring(2)) : decode(p[n].substring(2));
      }
      String actual = String.format(Locale.forLanguageTag(p[0]), decode(p[2]), values);
      if (!actual.equals(decode(p[3]))) {
        throw new AssertionError(p[0] + " " + p[1] + " exact-output mismatch");
      }
      count++;
    }
    int expectedCount = Integer.parseInt(args[1]);
    if (count != expectedCount) throw new AssertionError("Incorrect case count " + count);
    System.out.println(count + "/" + count + " actual JDK exact-output cases passed");
  }
}
