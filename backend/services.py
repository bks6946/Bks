import os
import logging
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from models import EbookContent, DownloadTracking, Statistics, Testimonial
from pdf_generator import PDFGenerator

logger = logging.getLogger(__name__)

class EbookService:
    def __init__(self, db, pdf_generator: PDFGenerator):
        self.db = db
        self.pdf_generator = pdf_generator
        self.ebook_content = self._get_default_content()
    
    def _get_default_content(self) -> Dict[str, Any]:
        """Get default ebook content"""
        return {
            "title": "Comment Faire 1000€ en 1 Mois en Étant Jeune",
            "subtitle": "Guide Complet pour Étudiants Entrepreneurs",
            "author": "EbookStudent",
            "pages": 87,
            "chapters": [
                {
                    "title": "Introduction : Pourquoi 1000€ en 1 Mois ?",
                    "description": "Découvrez pourquoi cet objectif est réaliste et comment l'atteindre en tant qu'étudiant.",
                    "content": [
                        {
                            "subtitle": "L'objectif réaliste de 1000€",
                            "text": [
                                "Gagner 1000€ en un mois peut sembler ambitieux, mais c'est tout à fait réalisable avec les bonnes stratégies. En tant qu'étudiant, vous avez des atouts uniques : la créativité, l'énergie et la capacité d'apprendre rapidement.",
                                "Ce guide ne vous promet pas de solutions miracles, mais des méthodes éprouvées que des milliers d'étudiants ont déjà utilisées avec succès. Chaque chapitre vous donnera des outils concrets pour diversifier vos sources de revenus.",
                                "L'important n'est pas seulement d'atteindre ce montant, mais de développer des compétences qui vous serviront toute votre vie professionnelle."
                            ],
                            "tips": "Commencez par fixer un objectif précis et réalisable. 1000€ en 30 jours = environ 33€ par jour. Cela devient plus gérable quand on le décompose ainsi !"
                        },
                        {
                            "subtitle": "Votre profil d'étudiant entrepreneur",
                            "text": [
                                "En tant qu'étudiant, vous avez des contraintes spécifiques : emploi du temps chargé, budget limité, mais aussi des avantages considérables. Vous êtes dans un environnement propice à l'apprentissage et à l'expérimentation.",
                                "Ce guide s'adapte à votre réalité : des méthodes qui s'intègrent dans votre planning étudiant, qui demandent peu ou pas d'investissement initial, et qui peuvent évoluer avec vos études.",
                                "Nous couvrirons des stratégies adaptées à différents profils : que vous soyez plutôt créatif, technique, commercial ou organisationnel."
                            ]
                        }
                    ]
                },
                {
                    "title": "Freelancing : Monétiser vos Compétences",
                    "description": "Apprenez à vendre vos services en ligne et à créer un profil attractif sur les plateformes de freelancing.",
                    "content": [
                        {
                            "subtitle": "Identifier vos compétences vendables",
                            "text": [
                                "Vous avez plus de compétences que vous ne le pensez ! Rédaction, traduction, design graphique, programmation, montage vidéo, community management... Même des compétences de base peuvent être monétisées.",
                                "Faites l'inventaire de vos compétences académiques et personnelles. Que savez-vous faire mieux que la moyenne ? Quels logiciels maîtrisez-vous ? Quelles langues parlez-vous ?",
                                "Les entreprises recherchent constamment des freelances pour des missions ponctuelles. Votre profil d'étudiant peut même être un atout : vous représentez la fraîcheur et l'innovation."
                            ],
                            "tips": "Commencez par lister 10 compétences que vous possédez, même basiques. Vous seriez surpris de voir combien sont recherchées sur le marché !"
                        },
                        {
                            "subtitle": "Créer un profil gagnant",
                            "text": [
                                "Votre profil sur les plateformes de freelancing (Upwork, Fiverr, 5euros.com) est votre vitrine. Une photo professionnelle, une description claire de vos services et des exemples de votre travail sont essentiels.",
                                "Rédigez une bio qui met en avant vos compétences uniques et votre motivation. Mentionnez votre statut d'étudiant comme un avantage : disponibilité, tarifs compétitifs, approche moderne.",
                                "Commencez par des tarifs attractifs pour obtenir vos premiers avis clients, puis augmentez progressivement vos prix en fonction de votre réputation."
                            ]
                        }
                    ]
                },
                {
                    "title": "Cours Particuliers et Tutorat",
                    "description": "Transformez vos connaissances académiques en revenus réguliers grâce aux cours particuliers.",
                    "content": [
                        {
                            "subtitle": "Choisir vos matières et niveaux",
                            "text": [
                                "Vous excellez dans certaines matières ? C'est votre ticket vers des revenus réguliers ! Les mathématiques, les sciences, les langues et l'informatique sont particulièrement demandées.",
                                "Ciblez les niveaux que vous maîtrisez parfaitement : collège, lycée, ou même première année universitaire. Mieux vaut être excellent sur un niveau que moyen sur plusieurs.",
                                "Calculez votre potentiel : 2 heures de cours par semaine à 20€/h = 160€/mois. Avec 4-5 élèves réguliers, vous atteignez facilement 600-800€ mensuels."
                            ],
                            "tips": "Commencez par proposer vos services à votre entourage : amis, famille, voisins. Le bouche-à-oreille est votre meilleur allié pour débuter !"
                        },
                        {
                            "subtitle": "Cours en ligne vs cours physiques",
                            "text": [
                                "Les cours en ligne vous permettent d'élargir votre zone de chalandise et d'optimiser votre temps. Pas de déplacements, horaires flexibles, et possibilité de donner cours à plusieurs élèves simultanément.",
                                "Les plateformes comme Superprof, Kelprof ou Acadomia facilitent la mise en relation avec des élèves. Vous pouvez également créer votre propre offre sur les réseaux sociaux.",
                                "Pour les cours physiques, concentrez-vous sur votre quartier ou votre campus. Les tarifs sont généralement plus élevés, mais vous avez moins d'élèves potentiels."
                            ]
                        }
                    ]
                },
                {
                    "title": "Jobs Étudiants Bien Rémunérés",
                    "description": "Découvrez les emplois étudiants qui offrent les meilleures rémunérations et conditions de travail.",
                    "content": [
                        {
                            "subtitle": "Les secteurs qui payent bien",
                            "text": [
                                "Tous les jobs étudiants ne se valent pas ! Certains secteurs offrent des rémunérations bien supérieures au SMIC. L'événementiel, l'hôtellerie haut de gamme, la garde d'enfants VIP, et les missions spécialisées sont particulièrement intéressantes.",
                                "Les jobs dans la tech (support technique, tests d'applications, modération) sont souvent bien payés et s'adaptent parfaitement aux étudiants en informatique.",
                                "Les missions ponctuelles (enquêtes, sondages, tests produits) peuvent rapporter entre 50 et 200€ par jour selon la complexité."
                            ],
                            "tips": "Inscrivez-vous sur plusieurs plateformes de jobs étudiants et créez des alertes pour les missions bien rémunérées. La rapidité de candidature fait souvent la différence !"
                        },
                        {
                            "subtitle": "Optimiser votre planning",
                            "text": [
                                "L'art du job étudiant, c'est de maximiser vos revenus tout en préservant vos études. Privilégiez les emplois flexibles qui s'adaptent à votre emploi du temps universitaire.",
                                "Concentrez-vous sur les créneaux les plus rentables : soirées, week-ends, vacances scolaires. Certains événements ponctuels peuvent vous rapporter l'équivalent d'une semaine de travail classique.",
                                "Négociez toujours vos horaires et votre rémunération. En tant qu'étudiant motivé et flexible, vous avez plus de pouvoir de négociation que vous ne le pensez."
                            ]
                        }
                    ]
                },
                {
                    "title": "Vente en Ligne et E-commerce",
                    "description": "Lancez votre activité de vente en ligne avec des investissements minimaux et des risques contrôlés.",
                    "content": [
                        {
                            "subtitle": "Dropshipping pour débutants",
                            "text": [
                                "Le dropshipping vous permet de vendre des produits sans les stocker. Vous jouez le rôle d'intermédiaire entre le fournisseur et le client final. C'est idéal pour débuter avec un budget limité.",
                                "Choisissez une niche que vous connaissez bien : gaming, beauté, fitness, tech... Votre passion vous donnera une expertise naturelle pour sélectionner les bons produits et communiquer efficacement.",
                                "Commencez petit avec 2-3 produits testés, puis élargissez votre catalogue en fonction des retours clients. Une boutique bien ciblée vaut mieux qu'un catalogue généraliste."
                            ],
                            "tips": "Testez toujours vos produits avant de les vendre. Commandés vous-même pour vérifier la qualité et les délais de livraison. Votre réputation en dépend !"
                        },
                        {
                            "subtitle": "Plateformes et marketing",
                            "text": [
                                "Shopify, WooCommerce, ou même Facebook Marketplace peuvent héberger votre boutique. Commencez par les solutions gratuites ou peu coûteuses avant d'investir dans des outils plus sophistiqués.",
                                "Le marketing sur les réseaux sociaux est votre arme secrète. Instagram, TikTok et Facebook vous permettent de toucher directement votre audience cible avec des budgets publicitaires maîtrisés.",
                                "Créez du contenu authentique autour de vos produits. Les vidéos de déballage, les tutoriels d'utilisation et les témoignages clients sont particulièrement efficaces."
                            ]
                        }
                    ]
                },
                {
                    "title": "Création de Contenu et Monétisation",
                    "description": "Transformez votre créativité en revenus grâce aux plateformes de contenu et aux partenariats.",
                    "content": [
                        {
                            "subtitle": "YouTube et TikTok : au-delà du divertissement",
                            "text": [
                                "Créer du contenu sur YouTube ou TikTok n'est plus réservé aux influenceurs. Vous pouvez monétiser votre expertise dans votre domaine d'études : tutoriels, conseils, vulgarisation scientifique...",
                                "La régularité est clé : mieux vaut publier une vidéo par semaine pendant 6 mois qu'une vidéo par jour pendant 3 semaines. Votre audience a besoin de constance pour s'attacher à votre contenu.",
                                "Diversifiez vos sources de revenus : publicités, sponsoring, affiliation, vente de produits dérivés. Ne dépendez jamais d'une seule source de monétisation."
                            ],
                            "tips": "Commencez par partager vos connaissances dans votre domaine d'études. Vous avez une expertise naturelle que beaucoup recherchent !"
                        },
                        {
                            "subtitle": "Blogging et rédaction web",
                            "text": [
                                "Un blog peut devenir une source de revenus passifs considérable. Choisissez un sujet qui vous passionne et dans lequel vous avez une expertise, même relative.",
                                "Monétisez votre blog avec l'affiliation, la publicité, la vente de produits numériques (ebooks, cours en ligne) ou les articles sponsorisés.",
                                "La rédaction web freelance est également très demandée. De nombreuses entreprises externalisent la création de leur contenu et recherchent des rédacteurs de qualité."
                            ]
                        }
                    ]
                },
                {
                    "title": "Applications et Micro-services",
                    "description": "Exploitez l'économie des applications mobiles et des micro-services pour générer des revenus complémentaires.",
                    "content": [
                        {
                            "subtitle": "Apps de services et tâches rémunérées",
                            "text": [
                                "Des applications comme Uber Eats, Deliveroo, ou TaskRabbit vous permettent de générer des revenus flexibles. Choisissez celles qui s'adaptent le mieux à votre situation et à vos disponibilités.",
                                "Les missions de livraison peuvent être très rentables aux bonnes heures (déjeuner, dîner, week-ends). Certains livreurs gagnent plus de 15€/heure en optimisant leurs créneaux.",
                                "Explorez aussi les applications de services à domicile : ménage, jardinage, bricolage, garde d'animaux. Vos compétences personnelles peuvent être monétisées."
                            ],
                            "tips": "Calculez toujours votre rentabilité réelle en déduisant les frais (essence, usure du véhicule, temps de trajet). L'optimisation de vos tournées est cruciale !"
                        },
                        {
                            "subtitle": "Micro-investissements et cashback",
                            "text": [
                                "Les applications de cashback et de micro-investissement peuvent compléter vos revenus. Rakuten, eBuyClub, ou Yuka pour les courses, Coinbase pour les cryptomonnaies...",
                                "Participez à des études de marché rémunérées. Votre profil d'étudiant est recherché par les entreprises qui veulent comprendre votre génération.",
                                "Certaines applications vous paient pour marcher, répondre à des sondages, ou tester des produits. Individuellement, les gains sont faibles, mais cumulés, ils peuvent représenter 50-100€/mois."
                            ]
                        }
                    ]
                },
                {
                    "title": "Optimisation Fiscale et Légale",
                    "description": "Comprenez vos obligations légales et optimisez votre situation fiscale en tant qu'étudiant entrepreneur.",
                    "content": [
                        {
                            "subtitle": "Statuts et déclarations",
                            "text": [
                                "En tant qu'étudiant, vous bénéficiez de certains avantages fiscaux, mais attention aux seuils ! Au-delà de certains montants, vous devez déclarer vos revenus et potentiellement perdre des avantages familiaux.",
                                "Le statut d'auto-entrepreneur est souvent le plus adapté pour débuter. Les démarches sont simplifiées et vous permet de facturer légalement vos services.",
                                "Tenez un registre précis de vos revenus et dépenses. Cela vous sera utile pour vos déclarations et vous permettra d'optimiser votre rentabilité."
                            ],
                            "tips": "Consultez un comptable ou un conseiller fiscal au moins une fois par an. Cet investissement vous fera souvent économiser plus que son coût !"
                        },
                        {
                            "subtitle": "Gestion de vos revenus",
                            "text": [
                                "Diversifiez vos sources de revenus pour réduire les risques. Ne dépendez jamais d'une seule activité, même si elle est très rentable.",
                                "Épargnez automatiquement une partie de vos revenus. Même 10-20% mis de côté chaque mois vous constitueront rapidement une réserve de sécurité.",
                                "Réinvestissez une partie de vos bénéfices dans votre développement : formations, outils, marketing. C'est ainsi que vous passerez de 1000€/mois à 2000€/mois."
                            ]
                        }
                    ]
                },
                {
                    "title": "Plan d'Action sur 30 Jours",
                    "description": "Votre roadmap détaillée pour atteindre l'objectif de 1000€ en suivant une stratégie progressive.",
                    "content": [
                        {
                            "subtitle": "Semaine 1 : Fondations",
                            "text": [
                                "Jours 1-2 : Faites le bilan de vos compétences et ressources. Identifiez 3 activités que vous pouvez commencer immédiatement.",
                                "Jours 3-4 : Créez vos profils sur les plateformes pertinentes (freelancing, cours particuliers, vente en ligne).",
                                "Jours 5-7 : Lancez vos premières actions : postez vos premiers services, contactez vos premiers prospects, créez votre premier contenu.",
                                "Objectif semaine 1 : 100-200€ de revenus potentiels identifiés et premiers pas concrets réalisés."
                            ],
                            "tips": "Ne cherchez pas la perfection dès le début. Mieux vaut lancer une offre imparfaite que de ne rien lancer du tout !"
                        },
                        {
                            "subtitle": "Semaines 2-3 : Accélération",
                            "text": [
                                "Optimisez vos premières actions en fonction des retours. Ajustez vos tarifs, améliorez vos descriptions, affinez votre ciblage.",
                                "Diversifiez vos sources de revenus. Si le freelancing fonctionne bien, maintenez-le mais ajoutez les cours particuliers ou la vente en ligne.",
                                "Automatisez ce qui peut l'être : réponses types, processus de commande, planification des publications sur les réseaux sociaux.",
                                "Objectif semaines 2-3 : 400-600€ de revenus générés et systèmes optimisés."
                            ]
                        },
                        {
                            "subtitle": "Semaine 4 : Finalisation",
                            "text": [
                                "Concentrez-vous sur les activités les plus rentables. Éliminez ou réduisez celles qui ne rapportent pas assez par rapport au temps investi.",
                                "Préparez le mois suivant : commandes récurrentes, clients fidélisés, contenu planifié à l'avance.",
                                "Analysez vos résultats et identifiez les axes d'amélioration pour reproduire et amplifier vos succès.",
                                "Objectif semaine 4 : Atteindre ou dépasser les 1000€ et avoir un système reproductible pour les mois suivants."
                            ]
                        }
                    ]
                },
                {
                    "title": "Bonus : Outils et Ressources",
                    "description": "Votre boîte à outils complète avec applications, sites web et ressources pour maximiser vos résultats.",
                    "content": [
                        {
                            "subtitle": "Applications indispensables",
                            "text": [
                                "Gestion : Notion (organisation), Todoist (tâches), Toggl (suivi du temps), Revolut (banque digitale)",
                                "Création : Canva (design), Grammarly (correction), Loom (vidéos), Unsplash (images gratuites)",
                                "Vente : Shopify (e-commerce), Mailchimp (email marketing), Hootsuite (réseaux sociaux), Stripe (paiements)"
                            ],
                            "tips": "Maîtrisez bien 2-3 outils plutôt que d'en utiliser 10 moyennement. L'efficacité vient de la maîtrise, pas de la quantité !"
                        },
                        {
                            "subtitle": "Plateformes et communautés",
                            "text": [
                                "Freelancing : Upwork, Fiverr, 5euros.com, Malt, Freelancer.com",
                                "Cours particuliers : Superprof, Kelprof, Acadomia, Coursenligne.fr",
                                "Vente : Facebook Marketplace, Vinted, Leboncoin, Amazon, Etsy",
                                "Communautés : Discord des entrepreneurs étudiants, groupes Facebook spécialisés, forums Reddit"
                            ]
                        }
                    ]
                }
            ]
        }
    
    async def get_ebook_content(self) -> Dict[str, Any]:
        """Get ebook content"""
        try:
            # Try to get from database first
            content = await self.db.ebook_content.find_one()
            if content:
                return content
            
            # Return default content if not found in database
            return self.ebook_content
        except Exception as e:
            logger.error(f"Error getting ebook content: {str(e)}")
            return self.ebook_content
    
    async def generate_pdf(self, user_agent: str, ip_address: str) -> str:
        """Generate PDF and return token"""
        try:
            # Get ebook content
            content = await self.get_ebook_content()
            
            # Generate PDF
            token = self.pdf_generator.generate_pdf(content)
            
            # Track download
            download_record = DownloadTracking(
                user_agent=user_agent,
                ip_address=ip_address,
                filename=f"ebook_{token}.pdf"
            )
            await self.db.download_tracking.insert_one(download_record.dict())
            
            return token
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise
    
    async def get_statistics(self) -> Statistics:
        """Get platform statistics"""
        try:
            total_downloads = await self.db.download_tracking.count_documents({})
            return Statistics(total_downloads=total_downloads)
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return Statistics()
    
    async def get_testimonials(self) -> List[Dict[str, Any]]:
        """Get testimonials"""
        try:
            testimonials = await self.db.testimonials.find().to_list(1000)
            if testimonials:
                return testimonials
            
            # Return default testimonials
            return [
                {
                    "name": "Marie L.",
                    "role": "Étudiante en Commerce",
                    "content": "J'ai réussi à gagner 1200€ en suivant les conseils sur le freelancing. Parfait pour financer mes études !",
                    "rating": 5
                },
                {
                    "name": "Thomas R.",
                    "role": "Étudiant en Informatique",
                    "content": "Les stratégies de vente en ligne m'ont permis de créer un complément de revenus stable. Très pratique !",
                    "rating": 5
                },
                {
                    "name": "Sarah M.",
                    "role": "Étudiante en Droit",
                    "content": "Guide très complet avec des méthodes réalistes. J'ai pu économiser pour mon voyage d'études.",
                    "rating": 5
                }
            ]
        except Exception as e:
            logger.error(f"Error getting testimonials: {str(e)}")
            return []