import { QuartzEmitterPlugin } from "../types"
import { write } from "./helpers"
import { FullSlug } from "../../util/path"

export const Robots: QuartzEmitterPlugin = () => ({
  name: "Robots",
  async *emit(ctx) {
    const baseUrl = ctx.cfg.configuration.baseUrl
    const sitemapLine = baseUrl ? `\nSitemap: https://${baseUrl}/sitemap.xml\n` : ""
    const content = `User-agent: *\nAllow: /\n${sitemapLine}`

    yield write({
      ctx,
      content,
      slug: "robots" as FullSlug,
      ext: ".txt",
    })
  },
  async *partialEmit() {},
})
