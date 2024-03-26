

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(ontable c)
(on d c)
(on e d)
(clear b)
(clear e)
)
(:goal
(and
(on a e)
(on c d)
(on d b)
(on e c))
)
)


