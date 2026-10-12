# Principal Nahuatl and Quechua choices

Decision recorded 12 October 2026 after the maintainer clarified that the main varieties should be used. This supersedes the proposed generic `nah` and `qu` choices. The earlier 162-option review remains historical source verification and does not accept the clarified scope.

## Bounded selection

Replace the two broad options with seven explicit choices:

| Tag | Picker label | Concrete scope |
|---|---|---|
| `nch` | Mexicano (Central Huasteca) | Central Huasteca Nahuatl |
| `nhe` | Náhuatl (Eastern Huasteca) | Eastern Huasteca Nahuatl |
| `nhw` | Náhuatl (Western Huasteca) | Western Huasteca Nahuatl |
| `quz` | Qichwa (Cusco) | Cusco Quechua |
| `quy` | Qichwa (Ayacucho / Chanka) | Ayacucho Quechua |
| `quh` | Qhichwa (South Bolivian) | South Bolivian Quechua |
| `qug` | Kichwa (Chimborazo) | Chimborazo Highland Quichua |

The name bases are source-supported; regional qualifiers use IANA-aligned English labels and are editorial disambiguators rather than a claim that the entire constructed label is a universally standardized autonym. All seven are individual-language tags in the [IANA registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry), File-Date 2026-09-17, with no deprecation. They should have exact `values-b+TAG/strings.xml` catalogues and unchanged public locale identities.

The arithmetic becomes **167 choices = 146 existing + 21 second-batch additions**. Relative to the original 140-choice source baseline, there are 27 additions, 59 full-key catalogues and 108 partial/empty catalogues. Registration still supplies no translated entries. Sanskrit `sa` retains its separately disclosed IANA macrolanguage scope; the clarification addressed Nahuatl and Quechua.

## Inclusion rationale and evidence

### Nahuatl

The [SIL Mexico linguistic guide](https://mexico.sil.org/es/publicaciones/confusion-de-nomenclatura/confusion-huasteco) identifies Huasteca as a major populous Nahuatl grouping and explicitly divides it into `nhe`, `nch` and `nhw`. Selecting that complete three-part cluster avoids treating a single Huasteca variety as all Nahuatl. [INALI's national catalogue](https://www.inali.gob.mx/sitios/clin-inali/html/l_nahuatl.html) separately lists the Huasteca veracruzana, Huasteca potosina and Huasteca hidalguense varieties and their self-designations. The first two include náhuatl; the Hidalgo entry includes mexicano.

This is a deliberately bounded principal cluster, not every Nahuatl variety. Guerrero, Puebla, central and other varieties must not be claimed as supported by those three tags. SIL's broad speaker estimate and older INALI variant figures are not interchangeable current census totals; no exact all-Nahuatl coverage percentage is claimed.

### Quechua, including Bolivia and Ecuador

Peru's [Ministry of Culture language record](https://bdpi.cultura.gob.pe/lenguas/quechua) treats Chanka and Collao as separate vital southern varieties with official writing support. Cusco and Ayacucho have specific IANA tags; the Cusco option must not be labelled as the whole broader Collao or Southern grouping. The ministry also [uses Chanka and Cusco-Collao in public information](https://www.gob.pe/institucion/cultura/noticias/49056-ministerio-de-cultura-y-asociacion-civil-transparencia-presentan-informacion-electoral-en-lenguas-indigenas). Peru's education publication [Urin Qichwa Qillqay](https://repositorio.perueduca.pe/recursos/2022/DEIB22-0568.pdf) supports the normalized name form Qichwa.

Bolivia is not represented merely by a Peruvian choice: `quh` explicitly registers South Bolivian Quechua. The Bolivian education ministry documents its own Qhichwa writing-normalization work, including *Qhichwa simip ñanchariynin*, in [its language-status publication, p. 113](https://biblioteca.minedu.gob.bo/biblio/eBooks/2019/October/5d9ceed9831b0/3_ESTADO_DE_SITUACION.pdf). This is a rationale for a distinct major Bolivian written choice, not a claim that `quh` covers North Bolivian Quechua or every Bolivian speech variety.

Ecuador is also included explicitly. Its [2024 government language-revitalization plan, printed p. 55](https://www.secretariapueblosynacionalidades.gob.ec/wp-content/uploads/2024/07/PLAN-DECENAL-DE-REVITALIZACION-Y-REVALORIZACION-DEL-USO-DE-LAS-LENGUAS-DE-LAS-NACIONALIDADES-DEL-ECUADOR2.pdf) maps Kichwa speakers using Census 2022 and reports the largest listed provincial total in Chimborazo (113,907). These are **provincial Kichwa counts, not a measured `qug` population**, and do not establish an exact percentage of Ecuadorian users covered. They support including a principal Ecuadorian choice while its label and tag stay specifically Chimborazo. The published PDF is too large for this web reader; the relevant primary-government map was available in indexed extraction. No full-document review is claimed.

A shared Southern Quechua written norm is real: [AmericasNLP's dataset authors](https://github.com/AmericasNLP/americasnlp2021/blob/main/data/quechua-spanish/README.md) describe its use and separately identify Cusco and Ayacucho data. That does not make `quz` a code for all Southern Quechua. No dedicated registered all-Southern language subtag was established in this review; the broader `qu` macrolanguage includes non-Southern varieties. The bounded concrete choices avoid silently promising universal Southern, Peruvian, Bolivian or Ecuadorian matching.

The set is practical initial coverage of major regional choices, not an exhaustive classification or definitive ranking of all varieties by speaker count. Other central, northern and Amazonian Quechua varieties remain outside this bounded set.

## Verification required after the edit

Recheck the new 167-option inventories, zero-entry exact catalogues, current 108-fallback counters, preservation of the prior 146 choices, absence of generic `nah`/`qu` options and their misleading coverage claims, precise per-variety labels and tracker rows. Preserve the original six-option and 140-choice historical evidence. All 21 second-batch translations and linguistic reviews remain unstarted; new source, host and hosted Android results must be bound to the revised source separately from the earlier 162-option candidate.
