#!/usr/bin/env node
/**
 * Generate VS Code preview screenshots for all Bloc themes.
 *
 * Usage:
 *   node scripts/generate-screenshots.mjs              # all themes
 *   node scripts/generate-screenshots.mjs carbon       # one theme
 *   node scripts/generate-screenshots.mjs carbon tsx    # one theme
 */

import { chromium } from "playwright";
import { mkdirSync, writeFileSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const TMP_DIR = join(__dirname, ".screenshot-tmp");
const OUT_DIR = join(ROOT, "screenshots");

const PALETTES = {
	Ash: ["#ACACAE", "#6E6E70", "#49494B", "#343436", "#2C2C2E", "#262628"],
	Stone: ["#928B88", "#605E5E", "#363636", "#2A2A2A", "#19191A", "#0A0A0A"],
	Slate: ["#CCCAD1", "#616565", "#3B403E", "#2B302E", "#1C2220", "#0C1212"],
	Carbon: ["#DBDBDB", "#999999", "#5F6062", "#373839", "#1F1F20", "#0A0A0A"],
	Midnight: ["#5D6880", "#3E4759", "#202937", "#14171E", "#0C1014", "#050304"],
	Sand: ["#EBD49D", "#A4A4A4", "#777674", "#4B4A48", "#262625", "#131313"],
	Graphite: ["#F7F7F7", "#C4C4C4", "#7F7F7F", "#404040", "#2E2E2E", "#232323"],
};

const ACCENTS = {
	Ash: {
		keyword: "#7AA2F7", operator: "#91B4F9", string: "#98C379", number: "#E5C07B",
		function: "#56B6C2", type: "#C678DD", constant: "#E06C75", tag: "#61AFEF",
		property: "#8FB6F3", parameter: "#6EC4CF", variable: "#B8BAC0", punctuation: "#7A7C80", decorator: "#D19A66",
	},
	Stone: {
		keyword: "#89B4FA", operator: "#9FC2FB", string: "#A6D189", number: "#E5C890",
		function: "#8CAAEE", type: "#CA9EE6", constant: "#E78284", tag: "#99D1DB",
		property: "#A5C4F7", parameter: "#7EB8D8", variable: "#B5B0AC", punctuation: "#787674", decorator: "#EF9F76",
	},
	Slate: {
		keyword: "#7FB4CA", operator: "#95C4D6", string: "#A3BE8C", number: "#EBCB8B",
		function: "#88C0D0", type: "#B48EAD", constant: "#D08770", tag: "#81A1C1",
		property: "#94BFD4", parameter: "#7ECAD8", variable: "#B8BCC0", punctuation: "#6E7472", decorator: "#EBCB8B",
	},
	Carbon: {
		keyword: "#5EA1FF", operator: "#7CB4FF", string: "#78C47B", number: "#F0B35E",
		function: "#4FB8CC", type: "#B684E0", constant: "#E06A8D", tag: "#6EA8FF",
		property: "#8EB4FF", parameter: "#67C6D4", variable: "#C8C8C8", punctuation: "#8A8B8D", decorator: "#DDAA66",
	},
	Midnight: {
		keyword: "#82AAFF", operator: "#9ABEFF", string: "#C3E88D", number: "#F78C6C",
		function: "#89DDFF", type: "#C792EA", constant: "#FF5370", tag: "#7FDBCA",
		property: "#96B8FF", parameter: "#7AD9F0", variable: "#A8B0C0", punctuation: "#5A6478", decorator: "#F78C6C",
	},
	Sand: {
		keyword: "#8AB4F8", operator: "#A0C3FA", string: "#8FB573", number: "#E6B566",
		function: "#78A6C8", type: "#B790C2", constant: "#C97A63", tag: "#6FA8DC",
		property: "#A0C0F0", parameter: "#86B8D4", variable: "#C4C0B8", punctuation: "#8A8884", decorator: "#D8A15B",
	},
	Graphite: {
		keyword: "#82AAFF", operator: "#99BBFF", string: "#A6E3A1", number: "#F9E2AF",
		function: "#89DCEB", type: "#CBA6F7", constant: "#F38BA8", tag: "#74C7EC",
		property: "#9EB8FF", parameter: "#7EDCE8", variable: "#D8D8D8", punctuation: "#949494", decorator: "#FAB387",
	},
};

const SHOTS = ["tsx"];
const THEMES = Object.keys(PALETTES);

function hexToRgb(hex) {
	const value = hex.replace("#", "");
	return [
		parseInt(value.slice(0, 2), 16),
		parseInt(value.slice(2, 4), 16),
		parseInt(value.slice(4, 6), 16),
	];
}

function resolveText(c1) {
	return hexToRgb(c1).reduce((a, b) => a + b, 0) > 400 ? c1 : "#E8E8E8";
}

function mix(a, b, ratio) {
	const ar = hexToRgb(a);
	const br = hexToRgb(b);
	const ch = (i) => Math.round(ar[i] + (br[i] - ar[i]) * ratio);
	return `#${ch(0).toString(16).padStart(2, "0")}${ch(1).toString(16).padStart(2, "0")}${ch(2).toString(16).padStart(2, "0")}`.toUpperCase();
}

function themeColors(name) {
	const [c1, c2, c3] = PALETTES[name];
	const accent = ACCENTS[name];
	const fg = resolveText(c1);
	const bright = hexToRgb(c1).reduce((a, b) => a + b, 0) > 400;

	return {
		bg0: PALETTES[name][5],
		bg1: PALETTES[name][4],
		bg2: PALETTES[name][3],
		bg3: c3,
		fg,
		fgMuted: c2,
		comment: bright ? c3 : c2,
		string: accent.string,
		number: accent.number,
		keyword: accent.keyword,
		operator: accent.operator,
		function: accent.function,
		type: accent.type,
		constant: accent.constant,
		tag: accent.tag,
		variable: accent.variable,
		parameter: accent.parameter,
		property: accent.property,
		attribute: mix(accent.property, accent.tag, 0.45),
		punctuation: accent.punctuation,
	};
}

function baseStyles(C) {
	return `
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1920px; height: 1080px; overflow: hidden;
    font-family: "SF Mono", "Menlo", "Monaco", "Consolas", monospace;
    font-size: 14px; line-height: 1.5; color: ${C.fg};
    background: ${C.bg0}; display: flex; flex-direction: column;
  }
  .titlebar {
    height: 30px; background: ${C.bg0}; display: flex;
    align-items: center; justify-content: center;
    color: ${C.fgMuted}; font-size: 12px;
    border-bottom: 1px solid ${C.bg0};
  }
  .main { display: flex; flex: 1; min-height: 0; }
  .activity {
    width: 48px; background: ${C.bg0}; display: flex;
    flex-direction: column; align-items: center; padding-top: 10px; gap: 18px;
  }
  .activity svg { opacity: 0.85; }
  .sidebar {
    width: 260px; background: ${C.bg0}; display: flex; flex-direction: column;
    border-right: 1px solid ${C.bg0};
  }
  .sidebar-header {
    padding: 10px 20px 8px; font-size: 11px; font-weight: 600;
    letter-spacing: 0.04em; color: ${C.fg};
  }
  .tree { padding: 0 8px; }
  .folder {
    display: flex; align-items: center; gap: 6px; padding: 3px 8px;
    color: ${C.fg}; font-size: 13px;
  }
  .file {
    display: flex; align-items: center; gap: 8px; padding: 3px 8px 3px 24px;
    font-size: 13px; color: ${C.fgMuted}; border-radius: 4px;
  }
  .file.active { background: ${C.bg3}; color: ${C.fg}; }
  .icon { width: 16px; height: 16px; flex-shrink: 0; }
  .editor-area { flex: 1; display: flex; flex-direction: column; min-width: 0; }
  .tabs {
    height: 35px; background: ${C.bg0}; display: flex; align-items: flex-end;
    padding-left: 8px;
  }
  .tab {
    height: 35px; padding: 0 16px; display: flex; align-items: center; gap: 8px;
    font-size: 13px; color: ${C.fgMuted}; background: ${C.bg0};
    border-top: 1px solid transparent;
  }
  .tab.active {
    color: ${C.fg}; background: ${C.bg1};
    border-top: 1px solid ${C.fg};
  }
  .tab-close { opacity: 0.5; font-size: 14px; }
  .editor-wrap { flex: 1; display: flex; min-height: 0; background: ${C.bg1}; }
  .gutter {
    width: 56px; background: ${C.bg1}; color: ${C.fgMuted};
    text-align: right; padding: 12px 12px 12px 0; font-size: 14px; line-height: 21px;
    user-select: none;
  }
  .gutter .active { color: ${C.fg}; }
  .code {
    flex: 1; padding: 12px 0; font-size: 14px; line-height: 21px;
    white-space: pre; overflow: hidden;
  }
  .minimap {
    width: 80px; background: ${C.bg1}; opacity: 0.35;
    border-left: 1px solid ${C.bg0};
  }
  .statusbar {
    height: 22px; background: ${C.bg2}; color: ${C.fg};
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 10px; font-size: 12px;
  }
  .status-left, .status-right { display: flex; gap: 16px; align-items: center; }
  .status-item { opacity: 0.95; }
  .cmt { color: ${C.comment}; font-style: italic; }
  .str { color: ${C.string}; }
  .num { color: ${C.number}; }
  .kw { color: ${C.keyword}; font-weight: 700; }
  .op { color: ${C.operator}; }
  .fn { color: ${C.function}; text-decoration: underline; }
  .ty { color: ${C.type}; font-style: italic; }
  .con { color: ${C.constant}; font-weight: 700; }
  .tag { color: ${C.tag}; }
  .var { color: ${C.variable}; }
  .param { color: ${C.parameter}; font-style: italic; }
  .prop { color: ${C.property}; }
  .attr { color: ${C.attribute}; }
  .punc { color: ${C.punctuation}; }
  .hl { background: ${C.bg3}48; }
`;
}

const cssIcon = `<svg class="icon" viewBox="0 0 16 16"><text x="2" y="12" fill="#519ABA" font-size="11" font-weight="700">#</text></svg>`;
const tsxIcon = `<svg class="icon" viewBox="0 0 16 16"><rect x="1" y="2" width="14" height="12" rx="1" fill="#519ABA"/><text x="2" y="11" fill="#FFFFFF" font-size="6" font-weight="700">TSX</text></svg>`;
const jsonIcon = `<svg class="icon" viewBox="0 0 16 16"><text x="1" y="12" fill="#CBCB41" font-size="10" font-weight="700">{ }</text></svg>`;

function fileRow(name, icon, active) {
	return `<div class="file${active ? " active" : ""}">${icon}<span>${name}</span></div>`;
}

function tab(name, active) {
	return `<div class="tab${active ? " active" : ""}"><span>${name}</span><span class="tab-close">x</span></div>`;
}

function statusBar(lang) {
	return `
    <div class="status-left">
      <span class="status-item">master*</span>
      <span class="status-item">0 errors 0 warnings</span>
    </div>
    <div class="status-right">
      <span class="status-item">${lang.line}</span>
      <span class="status-item">${lang.spaces}</span>
      <span class="status-item">UTF-8</span>
      <span class="status-item">LF</span>
      <span class="status-item">${lang.mode}</span>
    </div>
  `;
}

function shell(C, { themeLabel, sidebar, tabs, gutter, code, status }) {
	return `<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>${baseStyles(C)}</style></head>
<body>
  <div class="titlebar">test - Visual Studio Code</div>
  <div class="main">
    <div class="activity">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M3 5h7v7H3V5zm11 0h7v7h-7V5zM3 14h7v7H3v-7zm11 0h7v7h-7v-7z" fill="${C.fg}"/></svg>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><circle cx="10" cy="10" r="7" stroke="${C.fgMuted}" stroke-width="2"/><path d="M15 15l5 5" stroke="${C.fgMuted}" stroke-width="2"/></svg>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M7 4v16M12 4v16M17 4v16" stroke="${C.fgMuted}" stroke-width="2"/></svg>
    </div>
    <div class="sidebar">
      <div class="sidebar-header">EXPLORER</div>
      <div class="tree">${sidebar}</div>
    </div>
    <div class="editor-area">
      <div class="tabs">${tabs}</div>
      <div class="editor-wrap">
        <div class="gutter">${gutter}</div>
        <div class="code">${code}</div>
        <div class="minimap"></div>
      </div>
    </div>
  </div>
  <div class="statusbar">${status}</div>
</body></html>`;
}

function sidebarTree(active) {
	return `
    <div class="folder"><span>v</span><span>TEST</span></div>
    ${fileRow("test.css", cssIcon, active === "css")}
    ${fileRow("test.tsx", tsxIcon, active === "tsx")}
    ${fileRow("test.json", jsonIcon, active === "json")}
  `;
}

function gutterLines(start, count, activeLine) {
	return Array.from({ length: count }, (_, i) => {
		const n = start + i;
		const cls = n === activeLine ? "active" : "";
		return `<div class="${cls}">${n}</div>`;
	}).join("");
}

function buildShot(themeName, shot, C) {
	const sidebar = sidebarTree(shot);
	const tabsByShot = {
		tsx: [tab("test.json", false), tab("test.css", false), tab("test.tsx", true)].join(""),
	};

	const shots = {
		tsx: {
			gutter: gutterLines(1, 40, 18),
			code: `<span class="kw">import</span> { <span class="fn">useState</span> } <span class="kw">from</span> <span class="str">"react"</span>;

<span class="kw">type</span> <span class="ty">Task</span> = {
    <span class="prop">id</span>: <span class="ty">string</span>;
    <span class="prop">label</span>: <span class="ty">string</span>;
    <span class="prop">done</span>: <span class="ty">boolean</span>;
};

<span class="kw">export function</span> <span class="fn">TaskList</span>({ <span class="param">title</span> }<span class="punc">:</span> { <span class="prop">title</span><span class="punc">:</span> <span class="ty">string</span> }) {
    <span class="kw">const</span> [<span class="var">tasks</span>, <span class="var">setTasks</span>] = <span class="fn">useState</span><span class="op">&lt;</span><span class="ty">Task</span><span class="op">[]&gt;</span>([
        { <span class="prop">id</span><span class="punc">:</span> <span class="str">"1"</span>, <span class="prop">label</span><span class="punc">:</span> <span class="str">"Fix nav layout"</span>, <span class="prop">done</span><span class="punc">:</span> <span class="con">true</span> },
        { <span class="prop">id</span><span class="punc">:</span> <span class="str">"2"</span>, <span class="prop">label</span><span class="punc">:</span> <span class="str">"Add unit tests"</span>, <span class="prop">done</span><span class="punc">:</span> <span class="con">false</span> },
    ]);

    <span class="kw">const</span> <span class="fn">toggleTask</span> = (<span class="param">id</span><span class="punc">:</span> <span class="ty">string</span>) <span class="op">=&gt;</span> {
        <span class="fn">setTasks</span>((<span class="param">prev</span>) <span class="op">=&gt;</span>
            <span class="param">prev</span>.<span class="fn">map</span>((<span class="param">task</span>) <span class="op">=&gt;</span>
                <span class="param">task</span>.<span class="prop">id</span> <span class="op">===</span> <span class="param">id</span> <span class="op">?</span> { <span class="op">...</span><span class="param">task</span>, <span class="prop">done</span><span class="punc">:</span> <span class="op">!</span><span class="param">task</span>.<span class="prop">done</span> } <span class="op">:</span> <span class="param">task</span>,
            ),
        );
    };

    <span class="kw">return</span> (
        &lt;<span class="tag">section</span> <span class="attr">className</span>=<span class="str">"task-list"</span>&gt;
            &lt;<span class="tag">h2</span>&gt;{<span class="param">title</span>}&lt;/<span class="tag">h2</span>&gt;
            &lt;<span class="tag">ul</span>&gt;
                {<span class="var">tasks</span>.<span class="fn">map</span>((<span class="param">task</span>) <span class="op">=&gt;</span> (
                    &lt;<span class="tag">li</span> <span class="attr">key</span>={<span class="param">task</span>.<span class="prop">id</span>}&gt;
                        &lt;<span class="tag">input</span>
                            <span class="attr">type</span>=<span class="str">"checkbox"</span>
                            <span class="attr">checked</span>={<span class="param">task</span>.<span class="prop">done</span>}
                            <span class="attr">onChange</span>={() <span class="op">=&gt;</span> <span class="fn">toggleTask</span>(<span class="param">task</span>.<span class="prop">id</span>)}
                        /&gt;
                        &lt;<span class="tag">span</span>&gt;{<span class="param">task</span>.<span class="prop">label</span>}&lt;/<span class="tag">span</span>&gt;
                    &lt;/<span class="tag">li</span>&gt;
                ))}
            &lt;/<span class="tag">ul</span>&gt;
        &lt;/<span class="tag">section</span>&gt;
    );
}`,
			status: statusBar({ line: "Ln 18, Col 17", spaces: "Spaces: 4", mode: "{ TypeScript JSX }" }),
		},
	};

	const content = shots[shot];
	return shell(C, {
		themeLabel: themeName,
		sidebar,
		tabs: tabsByShot[shot],
		gutter: content.gutter,
		code: content.code,
		status: content.status,
	});
}

function resolveThemeArg(arg) {
	if (!arg) return null;
	const match = THEMES.find((t) => t.toLowerCase() === arg.toLowerCase());
	if (!match) {
		throw new Error(`Unknown theme "${arg}". Choose from: ${THEMES.join(", ")}`);
	}
	return match;
}

function resolveShotArg(arg) {
	if (!arg) return null;
	if (!SHOTS.includes(arg)) {
		throw new Error(`Unknown screenshot "${arg}". Choose from: ${SHOTS.join(", ")}`);
	}
	return arg;
}

async function main() {
	const themeFilter = resolveThemeArg(process.argv[2]);
	const shotFilter = resolveShotArg(process.argv[3]);
	const themes = themeFilter ? [themeFilter] : THEMES;
	const shots = shotFilter ? [shotFilter] : SHOTS;

	mkdirSync(TMP_DIR, { recursive: true });

	const browser = await chromium.launch();
	const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

	for (const themeName of themes) {
		const slug = themeName.toLowerCase();
		const themeDir = join(OUT_DIR, slug);
		mkdirSync(themeDir, { recursive: true });
		const C = themeColors(themeName);

		for (const shot of shots) {
			const html = buildShot(themeName, shot, C);
			const htmlPath = join(TMP_DIR, `${slug}-${shot}.html`);
			writeFileSync(htmlPath, html, "utf8");
			await page.goto(`file://${htmlPath}`, { waitUntil: "load" });
			await page.waitForTimeout(150);

			const outPath = join(themeDir, `${shot}.png`);
			await page.screenshot({ path: outPath, type: "png" });
			console.log(`Wrote ${outPath}`);

			if (themeName === "Carbon") {
				const rootPath = join(ROOT, `${shot}.png`);
				await page.screenshot({ path: rootPath, type: "png" });
				console.log(`Wrote ${rootPath}`);
			}
		}
	}

	await browser.close();
}

main().catch((err) => {
	console.error(err.message || err);
	process.exit(1);
});
