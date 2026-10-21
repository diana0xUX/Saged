/**
 * Nav consistency tests for saged.club
 * Journeys covered:
 *   J1  Home → Association (about.html)
 *   J2  Home → Join membership
 *   J3  Association → Home
 *   J4  Association → Join membership
 *   J5  Join → back to Association
 *   J6  Join → back to Home
 */

const http = require('http')

const PAGES = {
  home:   'http://localhost:8765/',
  about:  'http://localhost:8765/about.html',
  join:   'http://localhost:8765/join/'
}

function fetch(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let body = ''
      res.on('data', c => body += c)
      res.on('end', () => resolve({ status: res.statusCode, body }))
    }).on('error', reject)
  })
}

// ── Tiny HTML extractors (no DOM, no npm) ────────────────────────────────────

function allHrefs(html) {
  return [...html.matchAll(/href="([^"]+)"/g)].map(m => m[1])
}

function navHrefs(html) {
  // Grab everything inside <header ...> or <nav ...> up to its closing tag
  const navBlock = html.match(/<header[^>]*class="[^"]*nav[^"]*"[\s\S]*?<\/header>/i)
              || html.match(/<nav[\s\S]*?<\/nav>/i)
  if (!navBlock) return []
  return [...navBlock[0].matchAll(/href="([^"]+)"/g)].map(m => m[1])
}

function logoHref(html) {
  // logo wrapper link
  const m = html.match(/class="(?:logo|gn__logo|join-back)[^"]*"[^>]*>|<a[^>]*class="(?:logo|gn__logo|join-back)"/)
          || html.match(/<a[^>]*(?:logo|join-back)[^>]*>/)
  if (!m) return null
  // look for href on the same tag or immediately before
  const tag = html.match(/<a[^>]*(?:class="(?:logo|gn__logo|join-back)")[^>]*>/)
           || html.match(/<a[^>]*href="[^"]*"[^>]*class="(?:logo|gn__logo|join-back)"/)
  if (tag) {
    const h = tag[0].match(/href="([^"]+)"/)
    return h ? h[1] : null
  }
  return null
}

function ctaHref(html) {
  // Book a class / CTA button — pill or gn__cta
  const m = html.match(/<a[^>]*class="(?:[^"]*pill[^"]*|gn__cta)"[^>]*href="([^"]+)"/)
          || html.match(/<a[^>]*href="([^"]+)"[^>]*class="(?:[^"]*pill[^"]*|gn__cta)"/)
  return m ? m[1] : null
}

function ctaLabel(html) {
  const m = html.match(/<a[^>]*class="(?:[^"]*pill[^"]*|gn__cta)"[^>]*>([\s\S]*?)<\/a>/)
          || html.match(/<a[^>]*href="[^"]*"[^>]*class="(?:[^"]*pill[^"]*|gn__cta)"[^>]*>([\s\S]*?)<\/a>/)
  return m ? m[1].trim() : null
}

function navLinks(html) {
  const block = html.match(/<nav[^>]*class="[^"]*(?:nav__links|gn__links)[^"]*"[\s\S]*?<\/nav>/)
             || html.match(/<div[^>]*class="[^"]*nav__links[^"]*"[\s\S]*?<\/div>/)
  if (!block) return []
  return [...block[0].matchAll(/<a[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g)]
    .map(m => ({ href: m[1], label: m[2].trim() }))
}

function mobileToggle(html) {
  if (html.includes('class="gn__burger"')) return 'icon-hamburger (.gn__burger)'
  if (html.match(/class="menu"/)) return 'text-button (.menu)'
  return 'none'
}

function hasLangSelect(html) {
  return html.includes('lang-select') || html.includes('language-select')
}

function navClass(html) {
  const m = html.match(/<(?:header|nav)[^>]*class="([^"]+)"/)
  return m ? m[1] : 'not found'
}

// ── Journey assertions ────────────────────────────────────────────────────────

function canNavigateTo(hrefs, destination, label) {
  const target = destination.replace('http://localhost:8765', '')
  const found = hrefs.some(h => h === target || h === destination ||
    (target === '/' && h === '#top') || // same page = home page
    h.startsWith(target.replace(/\/$/, '')))
  return found
}

// ── Run ───────────────────────────────────────────────────────────────────────

async function run() {
  const pages = {}
  for (const [name, url] of Object.entries(PAGES)) {
    const res = await fetch(url)
    pages[name] = { url, status: res.status, html: res.body }
  }

  const findings = []
  const pass = []

  function FAIL(msg) { findings.push('  FAIL  ' + msg) }
  function PASS(msg) { pass.push('  pass  ' + msg) }
  function CHECK(ok, passMsg, failMsg) { ok ? PASS(passMsg) : FAIL(failMsg) }

  // ── Page availability ─────────────────────────────────────────────────────
  console.log('\n── Page availability ───────────────────────────────')
  for (const [name, p] of Object.entries(pages)) {
    CHECK(p.status === 200, `${name} responds 200`, `${name} is ${p.status} — not reachable`)
  }

  const home  = pages.home.html
  const about = pages.about.html
  const join  = pages.join.html

  const homeHrefs  = allHrefs(home)
  const aboutHrefs = allHrefs(about)
  const joinHrefs  = allHrefs(join)

  // ── Nav system consistency ────────────────────────────────────────────────
  console.log('\n── Nav system ───────────────────────────────────────')
  const homeNavClass  = navClass(home)
  const aboutNavClass = navClass(about)
  console.log(`  home  nav class: "${homeNavClass}"`)
  console.log(`  about nav class: "${aboutNavClass}"`)
  CHECK(homeNavClass === aboutNavClass,
    'same nav class across home and about',
    `nav class mismatch — home uses "${homeNavClass}", about uses "${aboutNavClass}" — two separate implementations`)

  // ── Logo href ─────────────────────────────────────────────────────────────
  console.log('\n── Logo href ─────────────────────────────────────────')
  const _getHref = (html, cls) => {
    const tag = html.match(new RegExp(`<a[^>]*${cls}[^>]*>`))
    return tag ? (tag[0].match(/href="([^"]+)"/) || [])[1] : null
  }
  const homeLogo    = _getHref(home, 'gn__logo')
  const aboutLogoHref = _getHref(about, 'gn__logo')
  const joinLogoHref  = _getHref(join, 'join-back')

  console.log(`  home  logo href: "${homeLogo}"`)
  console.log(`  about logo href: "${aboutLogoHref}"`)
  console.log(`  join  logo href: "${joinLogoHref}" (back-link, intentional)`)

  CHECK(homeLogo === '/',
    'home logo links to /',
    `home logo links to "${homeLogo}" — should be "/"`)

  CHECK(aboutLogoHref === '/',
    'about logo links to /',
    `about logo links to "${aboutLogoHref}"`)

  // ── Journey J1: Home → Association ────────────────────────────────────────
  console.log('\n── J1: Home → Association (about.html) ──────────────')
  const homeLinksToAbout = homeHrefs.some(h => h.includes('about.html') || h === '/about')
  CHECK(homeLinksToAbout,
    'J1 pass — home nav contains link to about.html',
    'J1 BROKEN — no link to about.html anywhere in home nav. Users cannot discover the association page.')

  // ── Journey J2: Home → Join ───────────────────────────────────────────────
  console.log('\n── J2: Home → Join (/join/) ──────────────────────────')
  const homeLinksToJoin = homeHrefs.some(h => h.includes('/join'))
  CHECK(homeLinksToJoin,
    'J2 pass — home links to /join/',
    'J2 no direct link from home to join')

  // ── Journey J3: Association → Home ────────────────────────────────────────
  console.log('\n── J3: Association → Home ────────────────────────────')
  const aboutLinksHome = aboutHrefs.some(h => h === '/' || h === 'index.html' || h === '#top')
  CHECK(aboutLinksHome,
    'J3 pass — about has link back to home',
    'J3 BROKEN — about.html has no link to home')

  // ── Journey J4: Association → Join ────────────────────────────────────────
  console.log('\n── J4: Association → Join (/join/) ───────────────────')
  const aboutLinksJoin = aboutHrefs.some(h => h.includes('/join'))
  CHECK(aboutLinksJoin,
    'J4 pass — about links to /join/',
    'J4 BROKEN — about.html has no link to /join/')

  // ── Journey J5: Join → Association ────────────────────────────────────────
  console.log('\n── J5: Join → Association (back link) ────────────────')
  const joinLinksAbout = joinHrefs.some(h => h.includes('about.html'))
  CHECK(joinLinksAbout,
    'J5 pass — join has back link to about.html',
    'J5 BROKEN — join has no link back to about.html')

  // ── Journey J6: Join → Home (by-design: join flows via about) ───────────────
  console.log('\n── J6: Join → Home (by design) ───────────────────────')
  const joinLinksHome = joinHrefs.some(h => h === '/' || h === '../' || h === 'index.html')
  console.log(`  join→home: ${joinLinksHome ? 'yes' : 'no (intentional — flow is home→about→join)'}`)

  // ── CTA destination ───────────────────────────────────────────────────────
  console.log('\n── CTA destination ───────────────────────────────────')
  const homeCTAHref  = _getHref(home, 'pill')
  const aboutCTATag  = about.match(/<a[^>]*gn__cta[^>]*>/)
  const aboutCTAHref = aboutCTATag ? (aboutCTATag[0].match(/href="([^"]+)"/) || [])[1] : null
  console.log(`  home  CTA href: "${homeCTAHref}"`)
  console.log(`  about CTA href: "${aboutCTAHref}"`)
  const homeIsWA  = homeCTAHref?.includes('wa.me')
  const aboutIsWA = aboutCTAHref?.includes('wa.me')
  if (!homeIsWA && aboutIsWA) FAIL(`CTA inconsistency: home "Book a class" → page anchor, about → WhatsApp. Users expect same action from same label.`)
  else PASS(`CTA destinations noted (home→anchor, about→WA — different contexts)`)

  // ── WhatsApp phone number consistency ─────────────────────────────────────
  console.log('\n── WhatsApp phone number ─────────────────────────────')
  const waNumbers = [...new Set(
    [...home.matchAll(/wa\.me\/(\d+)/g), ...about.matchAll(/wa\.me\/(\d+)/g), ...join.matchAll(/wa\.me\/(\d+)/g)]
    .map(m => m[1])
  )]
  console.log(`  numbers found across all pages: ${waNumbers.join(', ')}`)
  CHECK(waNumbers.length === 1,
    `single WA number used everywhere (${waNumbers[0]})`,
    `multiple WA numbers in use: ${waNumbers.join(' vs ')} — messages split across numbers`)

  // ── Nav link set consistency ────────────────────────────────────────────────
  console.log('\n── Nav link sets ─────────────────────────────────────')
  const homeLinks  = navLinks(home)
  const aboutLinks = navLinks(about)
  console.log(`  home  links: ${homeLinks.map(l => l.label).join(' | ')}`)
  console.log(`  about links: ${aboutLinks.map(l => l.label).join(' | ')}`)

  // Exclude CTA pill ("Book a class") — home has it as nav item, about has it as separate button
  const homeLabels  = homeLinks.map(l => l.label.replace(/\s*↗.*/, '').trim()).filter(l => l !== 'Book a class')
  const aboutLabels = aboutLinks.map(l => l.label.replace(/\s*↗.*/, '').trim())
  const onlyInHome  = homeLabels.filter(l => !aboutLabels.includes(l))
  const onlyInAbout = aboutLabels.filter(l => !homeLabels.includes(l))
  if (onlyInHome.length)  FAIL(`links only in home nav: [${onlyInHome.join(', ')}]`)
  if (onlyInAbout.length) FAIL(`links only in about nav: [${onlyInAbout.join(', ')}]`)
  if (!onlyInHome.length && !onlyInAbout.length) PASS('nav link labels match across pages')

  // ── Mobile toggle type ─────────────────────────────────────────────────────
  console.log('\n── Mobile toggle ─────────────────────────────────────')
  const homeMobile  = mobileToggle(home)
  const aboutMobile = mobileToggle(about)
  console.log(`  home  toggle: ${homeMobile}`)
  console.log(`  about toggle: ${aboutMobile}`)
  CHECK(homeMobile === aboutMobile,
    'mobile toggle type matches',
    `mobile toggle mismatch — home uses ${homeMobile}, about uses ${aboutMobile}`)

  // ── Language selector ──────────────────────────────────────────────────────
  console.log('\n── Language selector ─────────────────────────────────')
  const homeLang  = hasLangSelect(home)
  const aboutLang = hasLangSelect(about)
  console.log(`  home: ${homeLang ? 'yes' : 'no'}, about: ${aboutLang ? 'yes' : 'no'}`)
  if (homeLang !== aboutLang)
    FAIL(`lang selector present on home but not about — user loses language switching after clicking "Association"`)

  // ── Summary ────────────────────────────────────────────────────────────────
  console.log('\n══ RESULTS ═══════════════════════════════════════════')
  pass.forEach(p => console.log(p))
  if (findings.length === 0) {
    console.log('\n  All checks passed.\n')
  } else {
    console.log('\n── Inconsistencies found ─────────────────────────────')
    findings.forEach(f => console.log(f))
    console.log(`\n  ${findings.length} issue(s) to fix, ${pass.length} passed.\n`)
  }
}

run().catch(e => { console.error(e); process.exit(1) })
