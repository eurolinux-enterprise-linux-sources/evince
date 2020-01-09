/* -*- Mode: C; tab-width: 8; indent-tabs-mode: t; c-basic-offset: 8; c-indent-level: 8 -*- */
/*
 *  Copyright (C) 2004 Red Hat, Inc.
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
 */

#include "config.h"

#include "ev-document-find.h"

EV_DEFINE_INTERFACE (EvDocumentFind, ev_document_find, 0)

static void
ev_document_find_class_init (EvDocumentFindIface *klass)
{
}

GList *
ev_document_find_find_text (EvDocumentFind *document_find,
			    EvPage         *page,
			    const gchar    *text,
			    gboolean        case_sensitive)
{
	EvDocumentFindIface *iface = EV_DOCUMENT_FIND_GET_IFACE (document_find);
	
	return iface->find_text (document_find, page, text, case_sensitive);
}

