# Game Integration Notes

`lore.json` is the single source of truth for Parristan lore in any game build.

## Suggested use

- **Load once at startup** and read nation name, colours, currency and founders from it rather than hard-coding them.
- **Currency:** use `nation.currency` for the in-game wallet. Item prices in `items` are in Parri.
- **NPCs:** each founder in `founders` maps to an NPC by `id`. Keep dialogue and backstory in a separate file (e.g. `game/npc-dialogue.json`) so lore stays clean.
- **Laws:** good for a "Law of the Day" loading-screen tip or a quest where the player must obey (or cheekily break) a law.
- **Honours:** use as achievements.
- **Locations:** starter map nodes. Add more as the world grows.

## Example: loading in JavaScript

```js
const lore = await fetch('game/lore.json').then(r => r.json());
document.title = lore.nation.name;
const president = lore.founders.find(f => f.id === 'president');
console.log(`${president.name}, ${president.office}`);
```

## Rules for adding lore

1. Keep `lore.json` valid JSON (CI should check it).
2. Never add real-world contact details (addresses, phone numbers, emails) to lore files.
3. New laws, honours and ministries should be ratified at a National Assembly first, then added here.
