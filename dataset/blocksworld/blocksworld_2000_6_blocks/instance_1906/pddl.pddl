

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(ontable c)
(on d c)
(on e d)
(clear a)
(clear b)
(clear e)
)
(:goal
(and
(on b a)
(on c d)
(on d b)
(on e c))
)
)


