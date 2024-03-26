

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(on c a)
(ontable d)
(on e d)
(clear c)
(clear e)
)
(:goal
(and
(on d c)
(on e b))
)
)


