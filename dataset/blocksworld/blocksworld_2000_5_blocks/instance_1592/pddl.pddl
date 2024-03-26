

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c e)
(on d c)
(ontable e)
(clear a)
(clear b)
(clear d)
)
(:goal
(and
(on a b)
(on c a)
(on e d))
)
)


