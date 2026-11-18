# Supermodel REDUX V941 manual

Supermodel REDUX is a modular firmware for Elektron Model:Cycles. Windows Workbench lets you choose the machines, shared effects, and firmware add-ons you want. **Mask On** uses the Model:Cycles display conventions. Change Mask under **Settings → Global → Mask**.

[Support on Ko-fi](https://ko-fi.com/aveycole) · [Buy Me a Coffee](https://buymeacoffee.com/aveycole)

## Install with Windows Workbench

1. Download the Windows Workbench ZIP from this repository's release and extract the entire folder. Double-click **Supermodel Redux Workbench.exe**. The app opens the picker in your web browser and builds locally.
2. Put your official Model:Cycles OS 1.13 SysEx in the extracted folder at `reference/model-cycles_OS1.13.syx`. The builder checks the exact reference file before building. [Elektron Model:Cycles downloads](https://elektron.se/support-downloads/model-cycles)
3. Choose machines, shared FX, and optional add-ons. Drag machine rows or use the reorder grip with the arrow keys. Review the choices and use **Export configuration** to save a reusable JSON. **Load configuration** imports an earlier selection.
4. If you chose T9 HAT, add closed hat, open hat, crash, and ride WAVs. T9 CYMBAL needs crash and ride. Choose one encoding rate for the set. A lower rate or shorter samples leaves more room in the firmware image. LEGACY can use an imported 32-voice DX7 SysEx bank.
5. Click **Build firmware**. A successful build offers a **Download** for the resulting SysEx and enables **Flash** when a compatible Cycles is connected and stopped.
6. Connect the Cycles over USB, stop playback, and close other MIDI clients that are using its port. Under **Settings → Device → Transfer**, choose **CYC** for firmware. Click **Flash**. When the hardware shows **INSTALL OS?**, press **LEVEL/DATA**. Keep it powered and connected until it restarts.

The Workbench shows **Uploading**, **Checking image**, and **Install/restart** separately. The unit verifies the firmware before installation. A first install from stock can use the downloaded SysEx in Elektron Transfer. Keep backups of important projects before changing OS families. [Elektron OS update instructions](https://support.elektron.se/support/solutions/articles/43000662890-how-to-update-your-device)

## Panel and sequencing

| Control or feature | Use |
| --- | --- |
| LEVEL/DATA | Track level on Home. Turn to navigate a menu or edit its selected value. Press to select or confirm. |
| FUNC + LEVEL/DATA | Track pan. |
| MAIN VOLUME | Sets the main/headphone output. Mask On displays a segmented volume meter. |
| PLAY / STOP | Start or pause, and stop. Double STOP resets playback to the start. |
| RECORD and trig keys | Enter grid record and toggle steps. Hold a step and turn a control to enter a parameter lock. Hold multiple steps together to apply an edit to those steps. |
| PATTERN | Pick a pattern from the trig grid. Pattern Latch can keep this chooser open with a double press. BACK exits. |
| Direct Pattern Jump | Enable Global **JUMP**, then use FUNC with a pattern trig to jump directly. |
| PAGE | Select the active pattern page. Hold it during playback to engage Fill. |
| Fill 2 | Hold PAGE first, then FUNC. PAGE followed by TRACK latches Fill. |
| Trig Preview | While stopped, hold a step and press PAGE to audition it. |
| Trig Selection | TRACK + PAGE opens selection for editing groups across pages. |
| Page Length / Warp | Set 1–16 active steps per physical page. Warp preserves the page duration as its active step count changes. |
| Tempo / Swing / Chance | TEMPO opens the tempo page. Swing and Chance use the stock-style value display in Mask. Trig conditions, Chance, and other parameters can be locked on a step. |
| Groove Templates / Humanize | Pick a groove using FUNC with Swing. Groove templates combine timing and accents. Humanize introduces controlled timing variation. |
| Sequence Genie | Open the generator from the pattern workflow to create or vary a sequence. |
| Song | Arrange up to 32 rows with pattern repeats and track mute states. |
| Track Swap | Exchange tracks from the track settings while stopped. |
| Scale Lock | Constrain note entry to the selected scale. |
| Arpeggiator | Use the per-track arp controls for direction and octave range. |
| Chord Keys / Strum | Use the track's Chord Keys controls for diatonic trig chords. Strum offsets notes up to 80 ms either way. Chord and Wizard support strum. Chord, Velvet, and Wizard support Chord Keys. |
| Scramble | Randomize the selected track's enabled parameters. Use its track settings to choose which controls participate. |
| CTRL-ALL | Double TRACK to latch, select which tracks participate, and use BACK to undo. TRACK + SETTINGS opens Relative/Absolute Control Mode when selected in the builder. |
| Latching Mute | Set Global MUTE to LTC and use TRACK + FUNC. |
| Solo / Hold Mute | FUNC + pad solos a track when Solo is enabled. Hold Mute mutes a pad while held. |
| Quantized Mute | Set Global QNTM to decide when mute or solo changes take effect. |
| Punch / Gate | Toggle their per-track settings. Mask On updates the track state without opening an extra popup. |

## Machines

Press **MACHINES**, choose an engine with LEVEL/DATA, and confirm. **Silent machine browsing** and **Silent track selection** are optional picker features for navigating without auditioning. The machine-specific controls are labeled on their knob pages.

| Group | Engines |
| --- | --- |
| Stock | KICK, SNARE, METAL, PERC, TONE, CHORD |
| Redux synths | PUNCH, ELDER, ACID, ESTUS, RETROSYN, SHADOW, SPEAK, RING, LOFI, HEX, WAVE, VLVT, FERAL |
| Digital engines | MACRO, LEGACY |
| Percussion | TINY, SD VINTAGE, TRX-B2, TRX-SD, TRX-CH, SY TOY, CP VINTAGE, SY BITS, SY SWARM |
| T9 | BD, SD, HAT, CYMBAL, RIM / CLAP, TOM |
| Sampling / routing | SAMPLE WIZARD, MIDI OUT |

### Sample Wizard

Selecting Sample Wizard includes One Shot, Loop, Slice, Granular, Stretch, Pluck, Wave (wavetable), Chord, and the alternate pitch algorithms.

- **FUNC + MACHINES** opens the sample browser. The trig keys audition the highlighted sample. Press DATA to choose it or BACK to leave.
- **Hold SETTINGS + press MACHINES** opens the mode and setup menu. Turn DATA to move between rows. Press and turn DATA to change the value.
- **SETTINGS + PITCH** opens the pitch algorithms. Loop Setup provides traversal, bar sync, and crossfade. Slice Setup provides slice count, keyboard bank, marker editing, and undo. FUNC temporarily selects the next slice bank.
- Granular provides window shape, direction, and freeze. Stretch provides traversal and bar sync. Pluck provides sample, noise, or click excitation and string/drum choices. Wave and Chord expose harmony options in the mode setup.
- With grid recording on, hold step(s) and open **FUNC + MACHINES** to choose a sample lock. The track's ordinary sample continues to play on unlocked steps.
- The project stores sample references, settings, and locks. Keep the referenced samples on the drive for reload. Access resampling from Settings and use Transfer for supported sample upload/download.

## Shared FX and modulation

| Control | Use |
| --- | --- |
| Delay/Reverb Send | Set the current track's amount to each shared FX bus. |
| TRACK + DELAY TIME | Choose Off, Delay, Ping Pong, Crush, or Stop from the enabled delay-side FX. |
| TRACK + REVERB SIZE | Choose Off, Reverb, Hall, Chorus 1, Chorus 2, or Ring Mod from the enabled reverb-side FX. |
| DELAY TIME / feedback | Adjust delay time and use the secondary function for feedback. Optional Delay Notes displays musical note divisions, including triplets. |
| REVERB SIZE / tone | Adjust size and use the secondary function for tone. Stock Reverb is the first option after Off. |
| Crush | A dry-signal insert with rate and bit-depth controls. |
| Master Retrig | TRACK + RETRIG opens the master repeat. Double-tap to latch. Choose the repeat division in the panel view. Repeat FX Hold can pause shared effects during the repeat. |
| LFO | Open LFO Setup for the current track. PAGE selects among the enabled LFO slots in Redux. A held LFO and a supported parameter knob quick-assigns the selected slot. |
| LFO Amount | RETRIG + LFO SPEED adjusts amount for the selected slot when enabled. |
| Sidechain | Select the source track and its targets. Saved targets can include the shared FX buses. |
| Track Filter | Use the track filter controls for low/high mode, cutoff, resonance, and envelope. |
| Track Attack / Release | MACHINES + DECAY for attack. SETTINGS + DECAY for release. |

## Projects, MIDI, USB, and diagnostics

- **Settings → Project** opens project management. Use DATA to access the selected slot's load, save, or delete action. Back up before deleting. The project list fills in while you browse on an uncached drive. Verified names are reused and the latest saved project copy is read first.
- In Workbench **Transfer**, **Project backup** lists saved slots and exports `.rdxproj`; importing writes to an appropriate destination slot on the connected Cycles. **Convert a project** accepts a stock `.mcprj` or supported SysEx dumps and previews conversion before download or sending it to the device. Review warnings for fields the converter could not map.
- The **MIDI OUT** engine sends notes and CCs over the selected DIN/USB route. Use Settings → MIDI for clock and transport, routing, input filtering, and per-track channels. **MIDI OUT + THRU** adds BOTH to MIDI Ports when included. An empty route or a channel mismatch can leave an external track silent.
- **Settings → Device → USB mode** has **MID** for MIDI only, **A+M** for stereo audio and MIDI in Mask On, and **6CH** when six-channel USB is included. Six-channel mode maps one mono output to each track. Selecting a mode reconnects USB. Select the new channel layout in your host after it reconnects.
- **Settings → Audio Out** provides internal output routing and codec level settings. **HP MAX** caps headphone level. **INT OUT** controls internal output policy. **USB GAIN** is the level of computer audio played through the unit.
- **CPU diagnostics** is available when selected in the builder. The diagnostic shortcut is SETTINGS + BACK. **Device → USB Status** shows connection diagnostics. **Screen inversion** toggles regular/inverted display.

## Stock Base preview

Expand **Stock Base preview** in Workbench to build a separate firmware from your official OS 1.13 reference. Choose the patches, build its SysEx, and use the Cycles Startup Menu MIDI IN route as prompted. The preview uses the stock project format and panel workflow.

| Patch | Use |
| --- | --- |
| LFO 2, 3 & 4 | The first LFO press opens the stock page. Further LFO presses cycle through LFO 2, 3, and 4. BACK exits. Each slot has its own phase and settings per track. The preview stores the extra settings in RAM for the current session. |
| Latching track mute | Adds a latching mute mode. |
| Trig preview | Hold a step and press PAGE while stopped. |
| Scroll long browser names | Scrolls names too long for the browser row. |
| 546 BPM tempo limit | Raises the upper tempo range. |
| Chord Keys | Adds playable chord selection to the supported engine. |
| Numeric volume and pan | Shows numeric values for these track controls. |
| Dim trigless locks | Dims LEDs on steps that have locks without a trig. |
| Control All track selection | Choose which tracks Control All affects. |
| Master Retrig with latch | Adds a repeat across the master with a latch gesture. |
| Supermodel Redux and Cheddar Butt boot screens | Changes the boot artwork. |

The full Redux firmware has its own modular sound engines, project and transfer tools. Use the picker to choose the Full Redux or the Stock Base workflow that fits your setup.
