/* ev-document-fonts.h
 *  this file is part of evince, a gnome document_fonts viewer
 * 
 * Copyright (C) 2004 Red Hat, Inc.
 *
 * Author:
 *   Marco Pesenti Gritti <mpg@redhat.com>
 *
 * Evince is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Evince is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
 */

#include "config.h"

#include "ev-document-fonts.h"

EV_DEFINE_INTERFACE (EvDocumentFonts, ev_document_fonts, 0)

static void
ev_document_fonts_class_init (EvDocumentFontsIface *klass)
{
}

double
ev_document_fonts_get_progress (EvDocumentFonts *document_fonts)
{
	EvDocumentFontsIface *iface = EV_DOCUMENT_FONTS_GET_IFACE (document_fonts);

	return iface->get_progress (document_fonts);
}

gboolean
ev_document_fonts_scan (EvDocumentFonts *document_fonts,
			int              n_pages)
{
	EvDocumentFontsIface *iface = EV_DOCUMENT_FONTS_GET_IFACE (document_fonts);

	return iface->scan (document_fonts, n_pages);
}

void
ev_document_fonts_fill_model (EvDocumentFonts *document_fonts,
			      GtkTreeModel    *model)
{
	EvDocumentFontsIface *iface = EV_DOCUMENT_FONTS_GET_IFACE (document_fonts);

	iface->fill_model (document_fonts, model);
}
