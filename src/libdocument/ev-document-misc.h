/* -*- Mode: C; tab-width: 8; indent-tabs-mode: t; c-basic-offset: 8; c-indent-level: 8 -*- */
/*
 *  Copyright (C) 2000-2003 Marco Pesenti Gritti
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2, or (at your option)
 *  any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 *
 *  $Id$
 */

#if !defined (__EV_EVINCE_DOCUMENT_H_INSIDE__) && !defined (EVINCE_COMPILATION)
#error "Only <evince-document.h> can be included directly."
#endif

#ifndef EV_DOCUMENT_MISC_H
#define EV_DOCUMENT_MISC_H

#include <cairo.h>

#include <gdk-pixbuf/gdk-pixbuf.h>
#include <gtk/gtk.h>

G_BEGIN_DECLS

GdkPixbuf *ev_document_misc_get_thumbnail_frame  (int           width,
						  int           height,
						  GdkPixbuf    *source_pixbuf);
void       ev_document_misc_get_page_border_size (gint          page_width,
						  gint          page_height,
						  GtkBorder    *border);
void       ev_document_misc_paint_one_page       (GdkDrawable  *drawable,
						  GtkWidget    *widget,
						  GdkRectangle *area,
						  GtkBorder    *border,
						  gboolean      highlight);

cairo_surface_t *ev_document_misc_surface_from_pixbuf (GdkPixbuf *pixbuf);
GdkPixbuf       *ev_document_misc_pixbuf_from_surface (cairo_surface_t *surface);
cairo_surface_t *ev_document_misc_surface_rotate_and_scale (cairo_surface_t *surface,
							    gint             dest_width,
							    gint             dest_height,
							    gint             dest_rotation);

G_END_DECLS

#endif /* EV_DOCUMENT_MISC_H */
