"""All user-visible text, per language. Keys are shared by the page layout in build.py."""

EN = dict(
    lang="en", file="House_Assembly_Instructions",
    doc="Small House Model · Assembly Instructions",
    steps=["Long walls", "Gable walls", "Roof", "LED strip", "Fit the roof"],
    step_of="Step {n} of 5",
    glue="GLUE", noglue="NO GLUE", light="LIGHT",
    # cover
    cv_kicker="Assembly instructions", cv_title="Small House Model",
    cv_sub="Prefabricated wooden kit with LED-lit roof",
    cv_steps="steps", cv_parts="parts", cv_glue="wood glue required",
    # parts page
    p_kicker="Before you start", p_title="Parts, tools &amp; symbols",
    p_lead="Check that all parts are complete before you begin. The letters <b>A–H</b> are used in the steps.",
    p_ov="Overview (exploded view)", p_list="Parts list",
    lab_roof="Roof panel E", lab_eave="Eave rail G", lab_gable="Gable wall C", lab_long="Long wall B",
    lab_corner="Corner profile D",
    parts=["Long wall, 1 opening", "Long wall, 3 windows", "Gable wall (short wall)", "Corner profile",
           "Roof panel", "Ridge beam", "Eave rail (slotted)", "LED strip"],
    need_t="You will need",
    need=["Wood glue (PVA)", "Damp cloth for wiping off excess glue", "Clean, flat work surface",
          "Power supply for the LED strip"],
    sym_t="Symbols used",
    sym=["<b>Movement</b> – slide / move the part in the arrow direction",
         "<b>Glue</b> – apply wood glue at this joint",
         "<b>Do NOT glue</b> – dry fit only",
         "<b>Detail</b> – magnified view of a joint",
         "<b>Check</b> – result of the step"],
    # step 1
    s1_t="Glue the corner profiles to the long walls",
    s1_s="Each long wall gets a corner profile on both vertical edges.",
    s1_1="Take one long wall – <b>A</b> or <b>B</b>. The walls can be assembled <b>one at a time</b>; "
         "both are shown together here only to save space.",
    s1_2="Apply glue in the groove of a corner profile <b>D</b> and slide it onto the wall edge. "
         "Fit a profile on <b>both edges</b> of each long wall – <b>4</b> in total.",
    s1_3="Check that every profile is fully seated and straight. Wipe off excess glue and "
         "<b>let the glue dry</b> before continuing.",
    s1_n1="<b>How the profile works</b><br>Each corner profile has two grooves at 90°. In this step the long wall "
          "goes into one groove – the second groove stays free for the gable wall (Step 2).",
    s1_n2="<b>Result</b><br>Two long walls, each with a glued corner profile on both ends.",
    # step 2
    s2_t="Slide in the gable walls",
    s2_s="The two short gable walls are pushed into the free grooves of the corner profiles.",
    s2_1="Stand the long walls opposite each other.<br><br>Slide a gable wall <b>C</b> from above into the free "
         "grooves of the two corner profiles at each end of the house.",
    s2_2="Push the gable walls all the way down until they are fully seated in the profiles.<br><br>"
         "<b>Detail B:</b> long wall and gable wall meet in the corner profile.",
    s2_w="<b>Do NOT glue the gable walls.</b><br>They are a dry sliding fit in the corner profiles only. "
         "The walls are locked together when the roof is fitted in Step 5.",
    # step 3
    s3_t="Assemble the roof",
    s3_s="Two roof panels, one ridge beam and two eave rails are glued into one rigid roof.",
    lab_ridge="Ridge beam F", lab_eave2="Eave rail G", lab_2nd="for the 2nd panel",
    s3_1="Prepare the ridge beam <b>F</b> and the two slotted eave rails <b>G</b>.",
    s3_2="Glue the ridge beam along the <b>top edge</b> of the first roof panel <b>E</b>. Glue an eave rail on the "
         "inside, parallel to the lower edge, with the <b>slot facing down</b>.",
    s3_3="Glue the second eave rail to the second roof panel in the same way. Then glue the second panel against "
         "the ridge beam to close the roof. <b>Let the glue dry.</b>",
    s3_n1="<b>Keep the rails parallel</b><br>Both eave rails must be parallel to the ridge – they later slide onto "
          "the top edges of the long walls.",
    s3_n2="<b>Result</b><br>A rigid, glued roof with the ridge beam inside the apex.",
    # step 4
    s4_t="Mount the LED strip", s4_s="The LED strip lights the house from the inside of the roof.",
    lab_led="LED strip H", lab_led_sub="under the ridge beam",
    s4_1="Attach the LED strip <b>H</b> along the <b>underside of the ridge beam F</b>, centred along its full length.",
    s4_2="Turn the roof upside down. Press the strip firmly in place beneath the ridge beam so it is straight and "
         "does not sag.<br><br><b>Detail C:</b> LED strip in place under the ridge beam.",
    s4_n1="<b>Tip</b><br>Connect and test the LED strip <b>before</b> the roof is fitted on the house.",
    s4_n2="<b>Result</b><br>The LED strip sits under the ridge beam, facing down into the house.",
    # step 5
    s5_t="Fit the roof", s5_s="The slotted eave rails slide onto the top edges of the long walls.",
    s5_1="Hold the roof above the house with the eave rails over the long walls.<br><br>Slide the roof onto the "
         "<b>top edges of the long walls</b> – the wall tops engage in the slots of the eave rails <b>G</b>.",
    s5_2="Make sure the roof sits evenly on both long walls.<br><br><b>Your house is complete!</b> "
         "Connect the power and switch on the light.",
    s5_n="<b>Finished</b><br>Long walls glued to the corner profiles · gable walls dry fitted · glued roof with "
         "LED strip slid onto the long walls.",
)

NO = dict(
    lang="no", file="Hus_Monteringsanvisning",
    doc="Modellhus · Monteringsanvisning",
    steps=["Langvegger", "Kortvegger", "Tak", "LED-stripe", "Montere taket"],
    step_of="Trinn {n} av 5",
    glue="LIM", noglue="IKKE LIM", light="LYS",
    cv_kicker="Monteringsanvisning", cv_title="Modellhus",
    cv_sub="Ferdigkappede treelementer med LED-belyst tak",
    cv_steps="trinn", cv_parts="deler", cv_glue="krever trelim",
    p_kicker="Før du begynner", p_title="Deler, verktøy og symboler",
    p_lead="Kontroller at alle deler er med før du begynner. Bokstavene <b>A–H</b> brukes i trinnene.",
    p_ov="Oversikt (sprengskisse)", p_list="Deleliste",
    lab_roof="Takplate E", lab_eave="Takfotlist G", lab_gable="Kortvegg 1 (C)", lab_long="Langvegg 2 (B)",
    lab_corner="Hjørneprofil D",
    parts=["Langvegg 1 (1 åpning)", "Langvegg 2 (3 vinduer)", "Kortvegg 1 og kortvegg 2", "Hjørneprofil",
           "Takplate", "Mønebjelke", "Takfotlist (med spor)", "LED-stripe"],
    need_t="Du trenger",
    need=["Trelim (hvitlim)", "Fuktig klut til å tørke bort overflødig lim", "Ren og plan arbeidsflate",
          "Strømforsyning til LED-stripen"],
    sym_t="Symboler",
    sym=["<b>Bevegelse</b> – skyv / flytt delen i pilens retning",
         "<b>Lim</b> – påfør trelim i denne skjøten",
         "<b>IKKE lim</b> – monteres uten lim",
         "<b>Detalj</b> – forstørret visning av en skjøt",
         "<b>Kontroll</b> – resultatet av trinnet"],
    s1_t="Lim hjørneprofilene på langveggene",
    s1_s="Hver langvegg får en hjørneprofil på begge de loddrette kantene.",
    s1_1="Ta én langvegg – <b>langvegg 1 (A)</b> eller <b>langvegg 2 (B)</b>. Veggene kan monteres <b>én om gangen</b>; "
         "de vises sammen her bare for å spare plass.",
    s1_2="Påfør lim i sporet på en hjørneprofil <b>D</b> og skyv den inn på veggkanten. "
         "Monter en profil på <b>begge kantene</b> av hver langvegg – <b>4</b> til sammen.",
    s1_3="Kontroller at alle profilene sitter helt inne og står rett. Tørk bort overflødig lim og "
         "<b>la limet tørke</b> før du fortsetter.",
    s1_n1="<b>Slik virker profilen</b><br>Hver hjørneprofil har to spor i 90°. I dette trinnet går langveggen inn i "
          "det ene sporet – det andre sporet er ledig for kortveggen (trinn 2).",
    s1_n2="<b>Resultat</b><br>To langvegger, hver med en limt hjørneprofil i begge ender.",
    s2_t="Skyv inn kortveggene",
    s2_s="Kortvegg 1 og kortvegg 2 skyves inn i de ledige sporene i hjørneprofilene.",
    s2_1="Sett langveggene opp mot hverandre.<br><br>Skyv <b>kortvegg 1</b> og <b>kortvegg 2 (C)</b> ovenfra ned i de "
         "ledige sporene i de to hjørneprofilene i hver ende av huset.",
    s2_2="Skyv kortveggene helt ned til de sitter helt inne i profilene.<br><br>"
         "<b>Detalj B:</b> langvegg og kortvegg møtes i hjørneprofilen.",
    s2_w="<b>IKKE lim kortveggene.</b><br>De holdes kun på plass av sporene i hjørneprofilene. "
         "Veggene låses sammen når taket monteres i trinn 5.",
    s3_t="Sett sammen taket",
    s3_s="To takplater, én mønebjelke og to takfotlister limes sammen til ett stivt tak.",
    lab_ridge="Mønebjelke F", lab_eave2="Takfotlist G", lab_2nd="til takplate 2",
    s3_1="Legg fram mønebjelken <b>F</b> og de to takfotlistene <b>G</b> med spor.",
    s3_2="Lim mønebjelken langs <b>øvre kant</b> av den første takplaten <b>E</b>. Lim en takfotlist på innsiden, "
         "parallelt med nedre kant, med <b>sporet vendt ned</b>.",
    s3_3="Lim den andre takfotlisten på den andre takplaten på samme måte. Lim deretter den andre takplaten mot "
         "mønebjelken slik at taket lukkes. <b>La limet tørke.</b>",
    s3_n1="<b>Hold listene parallelle</b><br>Begge takfotlistene må være parallelle med mønet – de skal senere "
          "skyves inn på overkanten av langveggene.",
    s3_n2="<b>Resultat</b><br>Et stivt, limt tak med mønebjelken inne i mønet.",
    s4_t="Monter LED-stripen", s4_s="LED-stripen lyser opp huset fra innsiden av taket.",
    lab_led="LED-stripe H", lab_led_sub="under mønebjelken",
    s4_1="Fest LED-stripen <b>H</b> langs <b>undersiden av mønebjelken F</b>, sentrert over hele lengden.",
    s4_2="Snu taket opp ned. Trykk stripen godt fast under mønebjelken slik at den ligger rett og ikke henger "
         "ned.<br><br><b>Detalj C:</b> LED-stripen på plass under mønebjelken.",
    s4_n1="<b>Tips</b><br>Koble til og test LED-stripen <b>før</b> taket monteres på huset.",
    s4_n2="<b>Resultat</b><br>LED-stripen sitter under mønebjelken og lyser ned i huset.",
    s5_t="Monter taket", s5_s="Takfotlistene med spor skyves inn på overkanten av langveggene.",
    s5_1="Hold taket over huset med takfotlistene over langveggene.<br><br>Skyv taket inn på "
         "<b>overkanten av langvegg 1 og langvegg 2</b> – veggenes overkant går inn i sporene i takfotlistene <b>G</b>.",
    s5_2="Kontroller at taket ligger jevnt på begge langveggene.<br><br><b>Huset er ferdig!</b> "
         "Koble til strøm og slå på lyset.",
    s5_n="<b>Ferdig</b><br>Langvegger limt til hjørneprofilene · kortvegger montert uten lim · limt tak med "
         "LED-stripe skjøvet inn på langveggene.",
)
