class Snp(models.Model):
    rsid = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    code = models.CharField(max_length=500, blank=True, null=True)
    description_advanced = RichTextField(verbose_name="description", default="", blank=True, null=True)
    description_simple = RichTextField(default="", blank=True, null=True)
    importance = models.IntegerField(default=2, blank=True, null=True)
    genes = models.ManyToManyField(Gene, related_name="snps", through="SnpGenes")
    alleles = models.CharField(max_length=255, blank=True, null=True)
    ancestral_allele = models.CharField(max_length=500, blank=True, null=True)
    ambiguity_code = models.CharField(max_length=1, null=True, blank=True)
    minor_allele = models.CharField(max_length=255, blank=True, null=True, verbose_name="Minor Allele")
    minor_allele_frequency = models.FloatField(blank=True, null=True, verbose_name="Minor Allele Frequency")
    major_allele = models.CharField(max_length=255, blank=True, null=True, verbose_name="Major Allele")
    major_allele_frequency = models.FloatField(blank=True, null=True, verbose_name="Major Allele Frequency")
    bad_allele = models.CharField(max_length=1, blank=True, null=True)
    category = models.CharField(max_length=500, blank=True, null=True)
    genotype = models.CharField(max_length=500, blank=True, null=True)
    chromosome = models.CharField(max_length=500, blank=True, null=True)
    position = models.CharField(max_length=500, blank=True, null=True)
    locus = models.CharField(max_length=500, blank=True, null=True)
    allele_orientation = models.CharField(max_length=500, blank=True, null=True)
    heterozygous_color = models.CharField(max_length=500)
    homozygous_major_color = models.CharField(max_length=500)
    homozygous_minor_color = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    red_flag = models.BooleanField(default=False, blank=True)
    genotype_exceptions = models.CharField(max_length=255, blank=True, null=True, default="{}")
    chr_id = models.CharField(max_length=255, null=True, blank=True)
    chr_pos = models.CharField(max_length=255, null=True, blank=True)

    chr_start = models.IntegerField(null=True, blank=True, verbose_name="Chromosome Start")
    chr_end = models.IntegerField(null=True, blank=True, verbose_name="Chromosome End")
    strand = models.CharField(max_length=8, null=True, blank=True)
    ref_ncbi = models.CharField(max_length=32, null=True, blank=True)
    ref_ucsc = models.CharField(max_length=32, null=True, blank=True)
    observed = models.CharField(max_length=32, null=True, blank=True)
    func = models.CharField(max_length=255, null=True, blank=True)
    variation = models.CharField(max_length=255, null=True, blank=True)
    allele_ns = models.CharField(max_length=255, null=True, blank=True)

    snp_id_current = models.CharField(max_length=255, null=True, blank=True)
    gene_ids = models.CharField(max_length=255, null=True, blank=True)
    upstream_gene_id = models.IntegerField(null=True, blank=True)
    downstream_gene_id = models.IntegerField(null=True, blank=True)
    upstream_gene_distance = models.IntegerField(null=True, blank=True)
    downstream_gene_distance = models.IntegerField(null=True, blank=True)
    merged = models.IntegerField(null=True, blank=True)

    disease_variant = models.ManyToManyField("DiseaseVariant", blank=True)

    def __str__(self):
        return str(self.rsid)


class File(models.Model):
    FILE_STATUS_UPLOADED = "uploaded"
    FILE_STATUS_QUEUED = "queued"
    FILE_STATUS_PROCESSING = "processing"
    FILE_STATUS_ERROR = "error"
    FILE_STATUS_COMPLETED = "completed"
    FILE_STATUS_CHOICES = (
        (FILE_STATUS_UPLOADED, 'Uploaded',),
        (FILE_STATUS_QUEUED, 'Queued',),
        (FILE_STATUS_PROCESSING, 'Processing',),
        (FILE_STATUS_ERROR, 'Error',),
        (FILE_STATUS_COMPLETED, 'Completed',),
    )

    PROVIDER_UNKNOWN = 0
    PROVIDER_DIRECT_UPLOAD = 1
    PROVIDER_23ANDME_API = 2
    PROVIDER_CHOICES = (
        (PROVIDER_UNKNOWN, "Unknown"),
        (PROVIDER_DIRECT_UPLOAD, "Direct upload"),
        (PROVIDER_23ANDME_API, "23AndMe Api"),
    )

    SERVICE_UNKNOWN = 0
    SERVICE_23ANDME = 1
    SERVICE_ANCESTRY = 2
    SERVICE_COURTAGEN = 3
    SERVICE_FAMILY_TREE = 4
    SERVICE_VCF = 5
    SERVICE_CHOICES = (
        (SERVICE_UNKNOWN, "Unknown"),
        (SERVICE_23ANDME, "23AndMe"),
        (SERVICE_ANCESTRY, "Ancestry"),
        (SERVICE_COURTAGEN, "Courtagen"),
        (SERVICE_FAMILY_TREE, "Family Tree"),
        (SERVICE_VCF, "VCF"),
    )

    FILE_TYPE_CHOICES = (
        (0, "Default"),
        (1, "Demo"),
        (2, "Gene-Report"),
    )

    AGG_DATA_PROCESSION = (
        (0, 'Not available'),
        (1, 'In progress'),
        (2, 'Completed'),
    )

    file_name = models.CharField(max_length=500)
    original_name = models.CharField(max_length=255, null=True)
    hashed_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sequenced_at = models.CharField(max_length=500, blank=True, null=True)  # grab from the first line starting at :
    user = models.ForeignKey(User)
    genes_to_look_at = models.ManyToManyField(Gene, blank=True, through="UserGeneReputation")

    provider = models.IntegerField(choices=PROVIDER_CHOICES, default=0)
    file_type = models.IntegerField(choices=FILE_TYPE_CHOICES, default=0)
    service = models.IntegerField(choices=SERVICE_CHOICES, default=0)
    rescan_available = models.BooleanField(default=False)

    status = models.CharField(max_length=255, choices=FILE_STATUS_CHOICES, null=True, default=FILE_STATUS_UPLOADED)
    progress = models.FloatField(default=0, blank=True, null=True)
    status_message = models.TextField(blank=True, null=True)

    deleted_at = models.DateTimeField(null=True, blank=True)
    last_rescan_at = models.DateTimeField(null=True, blank=True)
    agg_data_available = models.IntegerField(
        choices=AGG_DATA_PROCESSION,
        help_text="individual's SNP data conclusions readiness",
        default=0
    )
    objects = FileManager()
    allfileobjects = models.Manager()

    def __init__(self, *args, **kwargs):
        self.progress_total_count = 0
        self.progress_total_index = 0
        self.progress_total = 0
        self.progress_delta = 0
        super(File, self).__init__(*args, **kwargs)

    def set_total_points(self, points, latency=100):
        self.progress_total_count = points if points > 0 else 1
        self.progress_delta = (100 - self.progress_total) / self.progress_total_count
        self.latency = latency

    def update_progress(self, val=None):
        """Updates the progress of the file processing.

        The progress is displayed to the user"""
        self.progress_total_index += 1
        self.progress_total += self.progress_delta
        if val:
            self.progress_total = val
        if self.progress_total_index % self.latency == 0 or val is not None:
            self.progress = self.progress_total
            if self.progress_total >= 100:
                self.status = self.FILE_STATUS_COMPLETED
            self.save()

    @property
    def is_demofile(self):
        return self.file_type == 1

    def __str__(self):
        return str(self.file_name)


class UserProfile(models.Model):
    COMPLEXITY = (
        ("reduced", "Reduced",),
        ("detailed", "Detailed",),
    )
    user = models.OneToOneField(User, related_name="user_profile")
    active_file = models.ForeignKey(File, blank=True, null=True, on_delete=models.DO_NOTHING)
    stripe_customer_id = models.CharField(max_length=500, blank=True, null=True)
    points = models.IntegerField(default=0)
    gene_packs = models.ManyToManyField(GenePack, related_name="gene_pack_user_profile", blank=True)
    gene = models.ManyToManyField(Gene, related_name="gene_user_profile", blank=True)
    symptoms = models.ManyToManyField("analysis.Symptom", related_name="user_profile_symptoms", blank=True,
                                      through="UserProfileSymptoms")
    conditions = models.ManyToManyField(Condition, related_name="user_profile_conditions", blank=True,
                                        through="UserProfileCondition")
    authorized_users = models.ManyToManyField(User, related_name="authorized_users", blank=True)
    traffic_source = models.CharField(max_length=500, blank=True, null=True)
    bookmarked_snps = models.ManyToManyField(Snp, related_name="bookmarked_snps", blank=True)
    related_objects = RelatedObjectsDescriptor()

    affiliated_from = models.ForeignKey("affiliate.AffiliateProfile", null=True, blank=True, related_name="affiliates")
    file_uploads_count = models.PositiveIntegerField(default=0, null=True)
    free_reports_available = models.IntegerField(default=0)
    free_reports_expiry = models.DateTimeField(null=True, blank=True)

    # 23AndMe Api
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    token_refresh_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Gene(models.Model):
    form = "GeneForm"
    name = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(max_length=500, null=True, blank=True)
    description_advanced = RichTextField(default="", null=True, blank=True)
    description_simple = RichTextField(default="", null=True, blank=True)
    fix_advanced = RichTextField(default="", null=True, blank=True)
    fix_simple = RichTextField(default="", null=True, blank=True)
    creator = models.CharField(max_length=500, blank=True, null=True)
    transcription_factors = models.ManyToManyField(TranscriptionFactor, related_name="gene_transcription_factors",
                                                   blank=True)
    diseasetraits = models.ManyToManyField("DiseaseTrait", through="GeneDiseaseTrait", related_name="genes", blank=True)
    function = models.TextField(null=True, blank=True)
    tissue_specificity = models.TextField(null=True, blank=True)
    induction = models.TextField(null=True, blank=True)
    miscellaneous = models.TextField(null=True, blank=True)
    developmental_stage = models.TextField(null=True, blank=True)
    caution = models.TextField(null=True, blank=True)
    enzyme_regulation = models.TextField(null=True, blank=True)
    cofactor = models.TextField(null=True, blank=True)
    keywords = models.ManyToManyField("GeneKeyword", related_name="genes", blank=True)
    pathways = models.ManyToManyField("GenePathway", related_name="genes", blank=True)
    global_pathways = models.ManyToManyField("Pathway", related_name="genes", blank=True,
                                             through="GeneDiseasePathwayInteraction")
    symbol = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.TextField(default="", null=True, blank=True)
    disgenet_geneid = models.CharField(max_length=255, null=True, blank=True)
    synonyms = models.ManyToManyField(Synonym, blank=True)
    disease_exceptions = models.ManyToManyField("DiseaseTrait", related_name="genes_exceptions", blank=True)
    exception_status = models.CharField(choices=EXCEPTION_STATUS, max_length=9, null=True, blank=True,
                                        verbose_name="Preferred Expression Status")
    ctd_id = models.CharField(max_length=255, null=True, blank=True)
    ctd_alt_gene_ids = models.TextField(default='', blank=True)
    ctd_bio_grid_ids = models.TextField(default='', blank=True)
    ctd_pharm_gkb_ids = models.TextField(default='', blank=True)
    ctd_uniprot_ids = models.TextField(default='', blank=True)

    protein_names = models.TextField(default='', blank=True)
    gene_encoded_by = models.TextField(default='', blank=True)
    natural_variant = models.TextField(default='', blank=True)
    length = models.TextField(default='', blank=True)
    polymorphysm = models.TextField(default='', blank=True)
    ec_number = models.TextField(default='', blank=True)
    catalytic_activity = models.TextField(default='', blank=True)
    kinetics = models.TextField(default='', blank=True)
    active_site = models.TextField(default='', blank=True)
    binding_site = models.TextField(default='', blank=True)
    metal_binding = models.TextField(default='', blank=True)
    dna_binding = models.TextField(default='', blank=True)
    nucleotide_binding = models.TextField(default='', blank=True)
    site = models.TextField(default='', blank=True)
    subunit_structure = models.TextField(default='', blank=True)
    go = models.ManyToManyField("GeneOntology", blank=True)
    pathology_allergenic = models.TextField(default='', blank=True)
    uniprot_biotechnological_use = models.TextField(default='', blank=True)
    uniprot_disruption_phenotype = models.TextField(default='', blank=True)
    uniprot_disease = models.TextField(default='', blank=True)
    uniprot_pharmacological_use = models.TextField(default='', blank=True)
    uniprot_toxic_dose = models.TextField(default='', blank=True)
    uniprot_subcellular_location = models.TextField(default='', blank=True)
    uniprot_peptide = models.TextField(default='', blank=True)
    uniprot_lipidation = models.TextField(default='', blank=True)
    uniprot_disulfide_bond = models.TextField(default='', blank=True)
    uniprot_zinc_finger = models.TextField(default='', blank=True)
    uniprot_protein_families = models.TextField(default='', blank=True)
    uniprot_domain = models.TextField(default='', blank=True)
    uniprot_motif = models.TextField(default='', blank=True)
    accessions_ensembl = models.TextField(default='', blank=True)
    accessions_pdb = models.TextField(default='', blank=True)
    accession_disgenet = models.TextField(default='', blank=True)
    accession_kegg = models.TextField(default='', blank=True)
    accession_ctd = models.TextField(default='', blank=True)
    accession_intac = models.TextField(default='', blank=True)
    accession_genewiki = models.TextField(default='', blank=True)

    ghr_function = RichTextField(default='', null=True, blank=True)
    is_loc = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']


class UserRsid(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    file = models.ForeignKey(File, related_name="related_rsid")
    rsid = models.CharField(max_length=500)
    chromosome = models.CharField(max_length=500)
    position = models.CharField(max_length=500)
    genotype = models.CharField(max_length=500)
    genotype_style = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.file)


class UserGeneReputation(models.Model):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    disease_risk_score = models.FloatField(default=0)

    @property
    def score_symbol(self):
        bad_weight = 3.7
        good_weight = 1.8
        if not self.score:
            return "U"
        elif self.score >= bad_weight:
            return "B"
        elif good_weight <= self.score < bad_weight:
            return "O"
        else:
            return "G"

    def __str__(self):
        return "%s <-> %s %s" % (self.file.user.username, self.gene.name, self.score,)

    class Meta:
        db_table = "genome_file_genes_to_look_at"
