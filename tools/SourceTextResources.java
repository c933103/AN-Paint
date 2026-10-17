/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import javax.xml.parsers.*;
import javax.xml.transform.*;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.*;

/** JDK source-launchable build tool; no extra runtime/build dependency. */
public class SourceTextResources {
    static final String PREFIX = "anpaint_source_";
    static final Pattern REFERENCE = Pattern.compile("^(\\s*)@string/([a-zA-Z0-9_]+)(\\s*)$");

    static Document parse(Path path) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
        factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        return factory.newDocumentBuilder().parse(path.toFile());
    }
    static void require(boolean condition, String message) {
        if (!condition) throw new IllegalArgumentException(message);
    }
    /** Validation view only: AAPT expands Unicode escapes after XML parsing.
     * Preserve emitted XML and existing conservative source spelling rules.
     * This is not a full AAPT whitespace/quoting decoder. Consume escaped pairs
     * once; a backslash produced by a Unicode escape is never decoded again.
     * Source contracts require four hex digits, including at end of text where
     * AAPT itself can also accept a shorter escape.
     */
    static String formatValidationText(String text) {
        StringBuilder result = new StringBuilder(text.length());
        for (int i = 0; i < text.length(); i++) {
            char value = text.charAt(i);
            if (value != '\\' || i + 1 == text.length()) { result.append(value); continue; }
            char escaped = text.charAt(++i);
            if (escaped != 'u') { result.append('\\').append(escaped); continue; }
            require(i + 4 < text.length(), "Source Unicode escapes require four hex digits");
            int code = 0;
            for (int digit = 1; digit <= 4; digit++) {
                int hex = "0123456789abcdef".indexOf(Character.toLowerCase(text.charAt(i + digit)));
                require(hex >= 0, "Invalid source Unicode escape");
                code = (code << 4) | hex;
            }
            result.append((char) code); i += 4;
        }
        return result.toString();
    }
    static void validateFormat(String text, boolean formatted) {
        require(text.length() <= 65536, "Source text exceeds runtime template bound");
        if (!formatted) return;
        text = formatValidationText(text);
        Object[] values = new Object[128];
        int position = 0, count = 0;
        while ((position = text.indexOf('%', position)) >= 0) {
            position++;
            require(++count <= 128, "Too many source placeholders");
            int digits = position;
            while (position < text.length() && Character.isDigit(text.charAt(position))) {
                require(position - digits < 4, "Source numeric field is too long");
                position++;
            }
            Integer index = null;
            if (position > digits && position < text.length() && text.charAt(position) == '$') {
                require(text.charAt(digits) != '0', "Source index starts at one");
                index = Integer.parseInt(text.substring(digits, position++)) - 1;
                require(index >= 0 && index < values.length, "Source argument index exceeds bound");
            } else position = digits;
            Set<Character> flags = new HashSet<>();
            while (position < text.length() && "-#+ 0,(<".indexOf(text.charAt(position)) >= 0) {
                require(flags.add(text.charAt(position++)), "Duplicate source format flag");
            }
            require(!flags.contains('<'), "Source arguments must have explicit indices");
            digits = position;
            while (position < text.length() && Character.isDigit(text.charAt(position))) {
                require(position - digits < 4, "Source width is too long");
                position++;
            }
            if (position > digits) require(Integer.parseInt(text.substring(digits, position)) <= 1024, "Source width exceeds bound");
            if (position < text.length() && text.charAt(position) == '.') {
                digits = ++position;
                while (position < text.length() && Character.isDigit(text.charAt(position))) {
                    require(position - digits < 3, "Source precision is too long");
                    position++;
                }
                require(position > digits, "Missing source precision");
                require(Integer.parseInt(text.substring(digits, position)) <= 128, "Source precision exceeds bound");
            }
            require(position < text.length(), "Missing source conversion");
            char conversion = text.charAt(position++);
            if (conversion != '%' && conversion != 'n') {
                require(index != null, "Source arguments must have explicit indices");
                Object value;
                switch (conversion) {
                    case 's': value = "value"; break;
                    case 'd': case 'X': value = 7L; break;
                    case 'f': value = 1.25; break;
                    default: throw new IllegalArgumentException("Unsupported source conversion: " + conversion);
                }
                require(values[index] == null || values[index].getClass() == value.getClass(), "Conflicting source argument types");
                values[index] = value;
            }
        }
        String.format(Locale.ROOT, text, values); // Validate flag/conversion combinations too.
    }
    static void visit(String name, Map<String, Set<String>> edges, Set<String> active, Set<String> done) {
        if (done.contains(name)) return;
        require(active.add(name), "Cyclic source text alias: " + name);
        for (String target : edges.getOrDefault(name, Set.of())) visit(target, edges, active, done);
        active.remove(name); done.add(name);
    }
    static boolean formatted(Element entry, Element value, Map<String, Element> entries) {
        if (entry.getAttribute("formatted").equals("false")) return false;
        Matcher reference = REFERENCE.matcher(value.getTextContent());
        if (!reference.matches()) return true;
        // Aliases were rebound above; carry the target's source contract too.
        Element target = entries.get("string/" + reference.group(2).substring(PREFIX.length()));
        return formatted(target, target, entries);
    }
    static void write(Document document, Path target) throws Exception {
        Files.createDirectories(target.getParent());
        Transformer transform = TransformerFactory.newInstance().newTransformer();
        transform.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
        transform.transform(new DOMSource(document), new StreamResult(target.toFile()));
    }
    public static void main(String[] args) throws Exception {
        require(args.length >= 2, "Usage: SourceTextResources.java RES_DIRECTORY OUTPUT_DIRECTORY [SOURCE_SET_RES_DIRECTORY...]");
        Path resources = Path.of(args[0]), output = Path.of(args[1]).toAbsolutePath().normalize();
        Set<Path> roots = new LinkedHashSet<>();
        roots.add(resources.toAbsolutePath().normalize());
        for (int i = 2; i < args.length; i++) roots.add(Path.of(args[i]).toAbsolutePath().normalize());
        // Only configured source-set resource roots are scanned, including app
        // and variant overlays. Absent conventional directories are legitimate.
        for (Path root : roots) {
            if (!Files.isDirectory(root) || root.startsWith(output)) continue;
            try (var paths = Files.walk(root)) {
                for (Path file : paths.filter(p -> !p.startsWith(output) && p.getFileName().toString().endsWith(".xml") &&
                        p.getParent().getFileName().toString().startsWith("values")).toList()) {
                    NodeList nodes = parse(file).getElementsByTagName("*");
                    for (int i = 0; i < nodes.getLength(); i++) {
                        Element node = (Element) nodes.item(i);
                        require(!node.getAttribute("name").startsWith(PREFIX), "Reserved source-text name in " + file);
                    }
                }
            }
        }
        Document document = parse(resources.resolve("values/strings.xml"));
        Map<String, Element> entries = new LinkedHashMap<>();
        NodeList children = document.getDocumentElement().getChildNodes();
        for (int i = 0; i < children.getLength(); i++) if (children.item(i) instanceof Element) {
            Element entry = (Element) children.item(i);
            require(Set.of("string", "plurals").contains(entry.getTagName()), "Source catalogue must contain strings/plurals only");
            String key = entry.getTagName() + "/" + entry.getAttribute("name");
            require(entries.putIfAbsent(key, entry) == null, "Duplicate source resource " + key);
        }
        Map<String, Set<String>> edges = new HashMap<>();
        for (var pair : entries.entrySet()) {
            Element entry = pair.getValue();
            List<Element> values = new ArrayList<>();
            if (entry.getTagName().equals("string")) values.add(entry);
            else {
                NodeList items = entry.getElementsByTagName("item");
                Set<String> forms = new HashSet<>();
                for (int i = 0; i < items.getLength(); i++) {
                    Element item = (Element) items.item(i);
                    require(forms.add(item.getAttribute("quantity")), "Duplicate English plural form");
                    values.add(item);
                }
                require(forms.equals(Set.of("one", "other")), "English source plurals require one and other");
            }
            for (Element value : values) {
                String text = value.getTextContent();
                Matcher reference = REFERENCE.matcher(text);
                if (reference.matches()) {
                    String target = "string/" + reference.group(2);
                    require(entries.containsKey(target), "Dangling source alias: " + target);
                    edges.computeIfAbsent(pair.getKey(), ignored -> new HashSet<>()).add(target);
                    value.setTextContent(reference.group(1) + "@string/" + PREFIX + reference.group(2) + reference.group(3));
                } else {
                    require(!text.strip().startsWith("@") && !text.strip().startsWith("?"), "Unsupported source reference: " + pair.getKey());
                    validateFormat(text, !entry.getAttribute("formatted").equals("false"));
                }
            }
            entry.setAttribute("name", PREFIX + entry.getAttribute("name"));
            entry.setAttribute("translatable", "false");
        }
        Set<String> done = new HashSet<>();
        for (String name : entries.keySet()) visit(name, edges, new HashSet<>(), done);
        Document contracts = DocumentBuilderFactory.newInstance().newDocumentBuilder().newDocument();
        Element root = contracts.createElement("resources");
        contracts.appendChild(root);
        Set<String> outputNames = new HashSet<>();
        for (var pair : entries.entrySet()) outputNames.add(pair.getKey().split("/", 2)[0] + "/" + pair.getValue().getAttribute("name"));
        for (var pair : entries.entrySet()) {
            Element source = pair.getValue();
            Element contract = contracts.createElement(source.getTagName());
            String name = PREFIX + "contract_" + pair.getKey().replace('/', '_');
            require(outputNames.add(source.getTagName() + "/" + name), "Source contract name collision");
            contract.setAttribute("name", name);
            contract.setAttribute("translatable", "false");
            contract.setAttribute("formatted", "false");
            if (source.getTagName().equals("string")) contract.setTextContent(Boolean.toString(formatted(source, source, entries)));
            else {
                NodeList items = source.getElementsByTagName("item");
                for (int i = 0; i < items.getLength(); i++) {
                    Element value = (Element) items.item(i);
                    Element item = contracts.createElement("item");
                    item.setAttribute("quantity", value.getAttribute("quantity"));
                    item.setTextContent(Boolean.toString(formatted(source, value, entries)));
                    contract.appendChild(item);
                }
            }
            root.appendChild(contract);
        }
        // Sync the generator-owned directory only after all inputs validate.
        if (Files.exists(output)) try (var paths = Files.walk(output)) {
            for (Path path : paths.sorted(Comparator.reverseOrder()).toList()) Files.delete(path);
        }
        write(document, output.resolve("values/source_text.xml"));
        write(contracts, output.resolve("values/source_text_contracts.xml"));
    }
}
