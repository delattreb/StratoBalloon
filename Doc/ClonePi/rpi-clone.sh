#!/bin/bash

PGM=`basename $0`

RSYNC_OPTIONS="--force -rltWDEgopt"

# List of extra dirs to create under /mnt.
OPTIONAL_MNT_DIRS="clone mnt sda sdb rpi0 rpi1"

# Where to mount the disk filesystems to be rsynced.
CLONE=/mnt/clone

CLONE_LOG=/var/log/$PGM.log

HOSTNAME=`hostname`

SRC_BOOT_PARTITION_TYPE=`parted /dev/mmcblk0 -ms p | grep "^1" | cut -f 5 -d:`
SRC_ROOT_PARTITION_TYPE=`parted /dev/mmcblk0 -ms p | grep "^2" | cut -f 5 -d:`

if [ `id -u` != 0 ]
then
    echo -e "Vous devez exécuter $PGM en tant que root (sudo).\n"
    exit 1
fi

if ! rsync --version > /dev/null
then
	echo -e "\nOoops! rpi-clone a besoin de rsync et ne peut pas le trouver0."
	echo "Vérifiez que rsync est installé :"
	echo "    $ apt-get update"
	echo -e "    $ apt-get install rsync\n"
	exit 0
fi

usage()
	{
	echo ""
	echo "Utilisation : $PGM sdN {-f|--force-initialize} {-v|--verbose}"
	echo "    Exemple : $PGM sda"
	echo "    -v - liste tous les fichiers lors de leur copie - Mode bavard."
	echo "    -f - force l'initialisation des partitions de desination"
	echo ""
	echo "    Clone (rsync) le système de fichiers d'un Raspberry Pi en fonctionnement"
	echo "    vers une carte SD de destination 'sdN' connectée à un port USB"
	echo "    du Raspberry Pi (via un lecteur de carte USB)."
	echo "    $PGM peut cloner le système en fonctionnement vers une nouvelle carte SD"
	echo "    ou peut faire une sauvegarde incrementielle (rsync) vers des cartes de sauvegardes existantes."
	echo ""
	echo "    Si la carte SD de destination possède une partition 1 $SRC_BOOT_PARTITION_TYPE partition 1 et une"
	echo "    partition 2 $SRC_ROOT_PARTITION_TYPE, $PGM suppose (sauf si vous avez utlilisé l'option -f)"
	echo "    que la carte SD est un backup précédent avec des partitions"
	echo "    correctement dimensionnées et configurées pour un Raspberry Pi.  Il suffit alors"
	echo "    de monter ces partitions et de les synchroniser avec le système en cours de fonctionnement."
	echo ""
	echo "    Si ces partitions n'existent pas (ou si vous avez utilisé -f), $PGM demande"
	echo "    si vous êtes d'accord pour initialiser les partitions sur la carte SD de destination."
	echo "    Ceci est réalisé avec un 'dd' partiel depuis la carte SD de démarrage"
	echo "    /dev/mmcblk0 vers la carte SD de destination /dev/sdN suivi par un"
	echo "    redimensionnement et un mkfs.ext4 de la partition 2 de /dev/sdN."
	echo "    Ceci crée une partition 1 $SRC_BOOT_PARTITION_TYPE contenant tous les fichiers"
	echo "    nécessaires au démarrage et une partition 2 rootfs vide mais ayant la taille attendue."
	echo "    Les partitions de la carte SD sont alors montées et synchronisées au système"
	echo "    en cours de fonctionnement."
	echo ""
	echo "    Les partitions de la carte SD de destination sont montées sur $CLONE."
	echo "    Un journal est écrit dans $CLONE_LOG pour faciliter un dépannage éventuel."
	echo "    Evitez de lancer des programmes qui écrivent sur le disque pendant l'exécution de $PGM."
	echo ""
	exit 0
	}

VERBOSE=off

while [ "$1" ]
do
	case "$1" in
		-v|--verbose)
			VERBOSE=on
			RSYNC_OPTIONS=${RSYNC_OPTIONS}v
			;;
		-f|--force-initialize)
			FORCE_INITIALIZE=true
			;;
		-h|--help)
			usage
			;;
		*)
			if [ "$DST_DISK" != "" ]
			then
				echo "Mauvais arguments"
				usage
			fi
			DST_DISK=$1
			;;
	esac
	shift
done


if [ "$DST_DISK" = "" ]
then
	usage
	exit 0
fi

if ! cat /proc/partitions | grep -q $DST_DISK
then
	echo "Le disque de destination '$DST_DISK' n'existe pas."
	echo "Connectez la carte SD à un port USB."
	echo "Si vous ne la voyez pas en '$DST_DISK', faites un"
	echo -e "'cat /proc/partitions' pour voir où elle peut être.\n"
	exit 0
fi

unmount_or_abort()
	{
	echo -n "Voulez vous démonter $1? (oui/non): "
	read resp
	if [ "$resp" = "o" ] || [ "$resp" = "oui" ]
	then
		if ! umount $1
		then
			echo "Désolé, $PGM ne peut pas démonter $1."
			echo -e "Fin du programme!\n"
			exit 0
		fi
	else
		echo -e "Fin du programme!\n"
		exit 0
	fi
	}

DST_ROOT_PARTITION=/dev/${DST_DISK}2
DST_BOOT_PARTITION=/dev/${DST_DISK}1

# Check that none of the destination partitions are busy (mounted).
#
DST_ROOT_CURMOUNT=`fgrep "$DST_ROOT_PARTITION " /etc/mtab | cut -f 2 -d ' ' `
DST_BOOT_CURMOUNT=`fgrep "$DST_BOOT_PARTITION " /etc/mtab | cut -f 2 -d ' ' `

if [ "$DST_ROOT_CURMOUNT" != "" ] || [ "$DST_BOOT_CURMOUNT" != "" ]
then
	echo "Une partition de destination est occupée (montée).  Status de montage:"
	echo "    $DST_ROOT_PARTITION:  $DST_ROOT_CURMOUNT"
	echo "    $DST_BOOT_PARTITION:  $DST_BOOT_CURMOUNT"
	if [ "$DST_BOOT_CURMOUNT" != "" ]
	then
		unmount_or_abort $DST_BOOT_CURMOUNT
	fi
	if [ "$DST_ROOT_CURMOUNT" != "" ]
	then
		unmount_or_abort $DST_ROOT_CURMOUNT
	fi
fi


TEST_MOUNTED=`fgrep " $CLONE " /etc/mtab | cut -f 1 -d ' ' `
if [ "$TEST_MOUNTED" != "" ]
then
	echo "Ce script utilise $CLONE pour monter les systèmes de fichiers, mais"
	echo "$CLONE est déja monté avec $TEST_MOUNTED."
	unmount_or_abort $CLONE 
fi

if [ ! -d $CLONE ]
then
	MNT_MOUNT=`fgrep " /mnt " /etc/mtab | cut -f 1 -d ' ' `
	if [ "$MNT_MOUNT" = "" ]
	then
		mkdir $CLONE
	else
		echo "$MNT_MOUNT est actuellement monté sur /mnt."
		unmount_or_abort /mnt
		mkdir $CLONE
	fi
fi


# Borrowed from do_expand_rootfs in raspi-config
expand_rootfs()
	{
	# Get the starting offset of the root partition
	PART_START=$(parted /dev/mmcblk0 -ms unit s p | grep "^2" | cut -f 2 -d:)
	[ "$PART_START" ] || return 1
	# Return value will likely be error for fdisk as it fails to reload the
	# partition table because the root fs is mounted
	fdisk /dev/$DST_DISK > /dev/null <<EOF
p
d
2
n
p
2
$PART_START

p
w
q
EOF
	}


# =========== Disk Setup and Checks ===========
#
# Check that destination partitions are the right type.
#
DST_BOOT_PARTITION_TYPE=`parted /dev/$DST_DISK -ms p \
		| grep "^1" | cut -f 5 -d:`
DST_ROOT_PARTITION_TYPE=`parted /dev/$DST_DISK -ms p \
		| grep "^2" | cut -f 5 -d:`


if [ "$DST_BOOT_PARTITION_TYPE" != "$SRC_BOOT_PARTITION_TYPE" ] || \
   [ "$DST_ROOT_PARTITION_TYPE" != "$SRC_ROOT_PARTITION_TYPE" ] || \
   [ "$FORCE_INITIALIZE" = "true" ]
then
	echo ""
	if [ "$FORCE_INITIALIZE" = "true" ]
	then
		echo "*** Forçage des partitions sur la destination '$DST_DISK' ***"
	fi

	echo "Les partitions existantes sur le disque de destination '$DST_DISK' sont:"
#	fdisk -l /dev/$DST_DISK | grep $DST_DISK
	parted /dev/$DST_DISK unit MB p \
		| sed "/^Model/d ; /^Sector/d"
	if [ "$DST_BOOT_PARTITION_TYPE" != "$SRC_BOOT_PARTITION_TYPE" ]
	then
		echo -e "  ... Impossible de trouver un système de fichier de démarrage de type: $SRC_BOOT_PARTITION_TYPE\n"
	fi
	if [ "$DST_ROOT_PARTITION_TYPE" != "$SRC_ROOT_PARTITION_TYPE" ]
	then
		echo -e "  ... Impossible de trouver un système de fichier root de type: $SRC_ROOT_PARTITION_TYPE\n"
	fi
	echo "Ce script peut initialiser la structure de partition du disque de destination"
	echo "en s'appuyant sur celle du système actuel et ensuite redmensionner"
	echo "la partition 2 (le système de fichiers racine) pour utiliser tout l'espace de la carte SD."
	echo -n "Voulez vous initialiser la destination /dev/$DST_DISK? (oui/non): "
	read resp
	if [ "$resp" = "o" ] || [ "$resp" = "oui" ]
	then
		# Image onto the destination disk a beginning fragment of the
		# running SD card file structure that spans at least more than
		# the start of partition 2.
		#
		# Calculate the start of partition 2 in MB for the dd.
		PART2_START=$(parted /dev/mmcblk0 -ms unit MB p | grep "^2" \
				| cut -f 2 -d: | sed s/MB// | tr "," "." | cut -f 1 -d.)
		# and add some slop
		DD_COUNT=`expr $PART2_START + 8`

		echo ""
		echo "Copie de la structure des partitions, copie de $DD_COUNT megaoctets..."
		dd if=/dev/mmcblk0 of=/dev/$DST_DISK bs=1M count=$DD_COUNT

		# But, though Partion 1 is now imaged, partition 2 is incomplete and
		# maybe the wrong size for the destination SD card.  So fdisk it to
		# make it fill the rest of the disk and mkfs it to clean it out.
		#
		echo "Redimensionnement de la partition 2 (système de fichiers racine) pour utiliser tout l'espace de la carte SD..."
		expand_rootfs
		mkfs.ext4 $DST_ROOT_PARTITION > /dev/null

		echo ""
		echo "/dev/$DST_DISK est initialisé et redimensionné. Ses partitions sont:"
#		fdisk -l /dev/$DST_DISK | grep $DST_DISK
		parted /dev/$DST_DISK unit MB p \
			| sed "/^Model/d ; /^Sector/d"

		SRC_ROOT_VOL_NAME=`e2label /dev/mmcblk0p2`
		echo ""
		echo "Vous avez démarré /dev/mmcblk0p2 nom du système de fichiers racine actuel: $SRC_ROOT_VOL_NAME"
		echo -n "Vous pouvez donner un nom au systèmes de fichiers racine destination $DST_ROOT_PARTITION: "
		read resp
		if [ "$resp" != "" ]
		then
			e2label $DST_ROOT_PARTITION $resp
		fi
	else
		echo -e "Aborting\n"
		exit 0
	fi
fi


# =========== Setup Summary ===========
#
DST_ROOT_VOL_NAME=`e2label $DST_ROOT_PARTITION`

if [ "$DST_ROOT_VOL_NAME" = "" ]
then
	DST_ROOT_VOL_NAME="no label"
fi

echo ""
echo "Disque destination cloné                     :  $DST_DISK"
echo "Systéme de fichiers racine destination cloné :  $DST_ROOT_PARTITION ($DST_ROOT_VOL_NAME) on ${CLONE}"
echo "Systéme de fichiers de démarrage cloné       :  $DST_BOOT_PARTITION on ${CLONE}/boot"
echo "Mode bavard                                  :  $VERBOSE"

echo "==============================="


# If this is an SD card initialization, can watch progress of the clone
# in another terminal with:  watch df -h
#
echo -n "Dernière vérification : Voulez vous vraiment lancer le clonage (oui/non)?: "
read resp
if [ "$resp" != "o" ] && [ "$resp" != "oui" ]
then
	echo -e "Interruption du programme de clonage.\n"
	exit 0
fi

#
# =========== End of Setup  ===========




# Mount destination filesystems.

echo "=> Montage de $DST_ROOT_PARTITION ($DST_ROOT_VOL_NAME) sur $CLONE"
if ! mount $DST_ROOT_PARTITION $CLONE
then
	echo -e "Impossible de monter $DST_ROOT_PARTITION, arrêt du programme!\n"
	exit 0
fi

if [ ! -d $CLONE/boot ]
then
	mkdir $CLONE/boot
fi

echo "=> Montage de $DST_BOOT_PARTITION sur $CLONE/boot"
if ! mount $DST_BOOT_PARTITION $CLONE/boot
then
	umount $CLONE
	echo -e "Impossible de monter $DST_BOOT_PARTITION, arrêt du programme!\n"
	exit 0
fi

echo "==============================="




START_TIME=`date '+%H:%M:%S'`

# Exclude fuse mountpoint .gvfs, various other mount points, and tmpfs
# file systems from the rsync.
#
sync
echo "Début de la synchronisation du système de fichiers vers $DST_DISK"
echo -n "(Soyez patient, ça peut prendre plusieurs minutes)..."
rsync $RSYNC_OPTIONS --delete \
		--exclude '.gvfs' \
		--exclude '/dev' \
		--exclude '/media' \
		--exclude '/mnt' \
		--exclude '/proc' \
		--exclude '/run' \
		--exclude '/sys' \
		--exclude '/tmp' \
		--exclude 'lost\+found' \
	// \
	$CLONE



# Fixup some stuff
#

for i in dev media mnt proc run sys
do
	if [ ! -d $CLONE/$i ]
	then
		mkdir $CLONE/$i
	fi
done

if [ ! -d $CLONE/tmp ]
then
	mkdir $CLONE/tmp
	chmod a+w $CLONE/tmp
fi

# Some extra optional dirs I create under /mnt
for i in $OPTIONAL_MNT_DIRS
do
	if [ ! -d $CLONE/mnt/$i ]
	then
		mkdir $CLONE/mnt/$i
	fi
done

rm -f $CLONE/etc/udev/rules.d/70-persistent-net.rules


DATE=`date '+%F %H:%M'`

echo "$DATE  $HOSTNAME $PGM : cloné sur $DST_DISK ($DST_ROOT_VOL_NAME)" \
		>> $CLONE_LOG
echo "$DATE  $HOSTNAME $PGM : cloné sur $DST_DISK ($DST_ROOT_VOL_NAME)" \
		>> $CLONE/$CLONE_LOG


STOP_TIME=`date '+%H:%M:%S'`

echo ""
echo "*** Clonage terminé sur /dev/$DST_DISK ***"
echo "    Début: $START_TIME    Fin: $STOP_TIME"
echo ""

# Pause before unmounting in case I want to inspect the clone results
# or need to custom modify any files on the destination SD clone.
# Eg. modify $CLONE/etc/hostname, $CLONE/etc/network/interfaces, etc
# if I'm cloning into a card to be installed on another Pi.
#
echo -n "Appuyez sur Entrée lorsque vous êtes prêt à démonter les partitions de /dev/$DST_DISK..."
read resp

echo "Démontage de $CLONE/boot"
umount $CLONE/boot

echo "Démontage de $CLONE"
umount $CLONE


echo "==============================="

exit 0
