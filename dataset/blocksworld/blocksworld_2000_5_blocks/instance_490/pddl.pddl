

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c a)
(on d b)
(on e c)
(clear d)
(clear e)
)
(:goal
(and
(on b e)
(on c a)
(on e d))
)
)


